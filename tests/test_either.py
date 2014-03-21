# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.actions import either
from monad.decorators import failsafe
from monad.exceptions import ExtractError
from monad.types import Either, Left, Right

test_range = range(-100, 100)
unit = Either.unit

error = Left('Error')


def add_1(n):
    if isinstance(n, int):
        return unit(n + 1)
    else:
        return error


def double(n):
    if isinstance(n, int):
        return unit(n * 2)
    else:
        return error


def fail(n):
    return error


def test_local_helper_function_add_one():
    for n in test_range:
        assert add_1(n) == unit(n + 1)
    assert add_1('1') is error


def test_local_helper_function_double():
    for n in test_range:
        assert double(n) == unit(n * 2)
    assert double('1') is error


def test_local_helper_function_fail():
    for n in test_range:
        assert fail(n) is error


def test_fmap_functor_laws():
    identity = lambda a: a
    f = lambda a: a + 1
    g = lambda a: a * 2
    f_g = lambda n: f(g(n))

    for n in test_range:
        ft = unit(n)
        # fmap id == id
        assert ft.fmap(identity) == identity(ft)
        # fmap (f . g) == fmap f . fmap g
        assert ft.fmap(f_g) == ft.fmap(g).fmap(f)

    value = 42
    l = Left('Something wrong.')
    r = Right(value)
    assert l.fmap(f) is l
    assert r.fmap(f) == Right(f(42))


def test_unit():
    assert type(unit(42)) is Right


def test_either_is_abstract():
    with pytest.raises(NotImplementedError):
        Either(42)


def test_compare():
    for n in test_range:
        assert Left(n) == Left(n)
        assert Right(n) == Right(n)
        assert Left(n) != Right(n)


def test_ordering():
    with pytest.raises(TypeError):
        Left(1) < 1

    with pytest.raises(TypeError):
        Right(1) < 1

    for n in test_range:
        assert (Left(n) < Left(n)) is False
        assert Left(n) > Left(n - 1)
        assert Left(n) < Left(n + 1)
        assert (Right(n) < Right(n)) is False
        assert Right(n) > Right(n - 1)
        assert Right(n) < Right(n + 1)
        assert Left(n) < Right(n)


def test_as_context_manager():
    for n in test_range:
        with pytest.raises(ExtractError):
            with unit(n) >> double >> fail >> double as result:
                assert False
                assert result

    with pytest.raises(ExtractError):
        with error as n:
            assert False

    with pytest.raises(ExtractError):
        with double(n) as result:
            with error as n:
                assert False

    with pytest.raises(ExtractError):
        with double(n) as result, error as n:
            assert False


def test_bool():
    assert bool(Left(True)) is False
    assert bool(Right(False)) is True
    for n in test_range:
        assert bool(Left(n)) is False
        assert bool(Right(n)) is True
        assert bool(unit(n)) is True


def test_bind():
    assert error.bind(add_1) is error
    for n in test_range:
        m = unit(n)
        assert m.bind(fail) is error


def test_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> fail is error
        assert fail(n) >> add_1 is error


def test_reversed_bind_operator():
    for n in test_range:
        m = unit(n)
        assert fail << m is error
        assert add_1 << fail(n) is error


def test_chain_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> fail >> add_1 == error
        assert m >> add_1 >> fail == error
        assert m >> fail >> double == error
        assert m >> double >> fail == error


def test_monad_law_left_identity():
    for n in test_range:
        # unit n >>= f == f n
        f = fail
        assert unit(n) >> f == f(n)


def test_monad_law_right_identity():
    for n in test_range:
        # m >>= unit == m
        assert error >> unit == error


def test_monad_law_associativity():
    for n in test_range:
        # m >>= (\x -> k x >>= h)  ==  (m >>= k) >>= h
        m = unit(n)
        k = add_1
        h = fail
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = fail
        h = double
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = fail
        h = fail
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h


def test_either_action():
    inc = lambda n: n + 1
    dec = lambda n: n - 1

    act = either(inc)
    assert act(Left(1)) == 2
    assert act(Right(1)) == 1

    act = either(left_handler=inc, right_handler=dec)
    assert act(Left(1)) == 2
    assert act(Right(1)) == 0


def test_either_action_with_incompatible_type():
    inc = lambda n: n + 1

    act = either(inc)
    assert act(Left(1)) == 2

    with pytest.raises(TypeError):
        act(1)


def test_failsafe_decorator():
    @failsafe
    def div(a, b):
        return a / b

    assert div(42, 21) == unit(2)
    assert isinstance(div(42, 0), Left)


def test_failsafe_decorator_catch_extract_error():
    @failsafe(left_on_exception=None)
    def wrong():
        with fail(1) as result:
            assert result is False  # should not reach here

    assert wrong() == error

    @failsafe(left_on_exception=None)
    def wrong():
        raise ExtractError('not a left')

    assert isinstance(wrong(), Left)


def test_failsafe_decorator_with_predicate():
    @failsafe(predicate=bool)
    def truth(x):
        return x

    assert truth(42) == unit(42)
    assert truth(None) == Left(None)
    assert add_1(0) >> truth == unit(1)
    assert add_1(-1) >> truth == Left(0)
    assert truth(False) >> double == Left(False)
    assert double([]) >> truth == error


def test_failsafe_decorator_with_value():
    @failsafe(left_on_value=None)
    def truth(x):
        return x

    assert truth(42) == unit(42)
    assert truth('') == unit('')
    assert truth(0) == unit(0)
    assert truth(False) == unit(False)
    assert truth(None) == Left(None)


def test_failsafe_decorator_combined():
    @failsafe(predicate=bool, left_on_value=42)
    def wrap(x):
        return x

    assert wrap(True) == Right(True)
    assert wrap(False) == Left(False)
    assert wrap('something') == Right('something')
    assert wrap('') == Left('')
    assert wrap([False]) == Right([False])
    assert wrap([]) == Left([])
    assert wrap(1) == Right(1)
    assert wrap(0) == Left(0)
    assert wrap(None) == Left(None)
    assert wrap(42) == Left(42)


def test_failsafe_decorator_none_exception():
    @failsafe(left_on_exception=None)
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(42, 0)


def test_failsafe_decorator_empty_seq_exception():
    for empty in ([], tuple(), set()):
        @failsafe(left_on_exception=empty)
        def div(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            div(42, 0)


def test_failsafe_decorator_specific_exception():
    @failsafe(left_on_exception=ZeroDivisionError)
    def div(a, b):
        return a / b

    assert isinstance(div(42, 0), Left)


def test_failsafe_decorator_specific_exception_tuple():
    @failsafe(left_on_exception=(IOError, ZeroDivisionError))
    def div(a, b):
        if a < 0:
            raise IOError
        return a / b

    assert isinstance(div(42, 0), Left)
    assert isinstance(div(-42, 2), Left)
