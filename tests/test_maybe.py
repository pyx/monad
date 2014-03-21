# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.actions import first
from monad.decorators import maybe
from monad.exceptions import ExtractError
from monad.types import Maybe, Just, Nothing

test_range = range(-100, 100)
unit = Maybe.unit


def add_1(n):
    if isinstance(n, int):
        return unit(n + 1)
    else:
        return Nothing


def double(n):
    if isinstance(n, int):
        return unit(n * 2)
    else:
        return Nothing


def fail(n):
    return Nothing


def test_local_helper_function_add_one():
    for n in test_range:
        assert add_1(n) == unit(n + 1)
    assert add_1('1') is Nothing


def test_local_helper_function_double():
    for n in test_range:
        assert double(n) == unit(n * 2)
    assert double('1') is Nothing


def test_local_helper_function_fail():
    for n in test_range:
        assert fail(n) is Nothing


def test_type():
    assert unit(1) == Just(1) == Maybe(1)
    assert Nothing != unit(1)
    assert type(unit(1)) == type(Just(1)) == type(Maybe(1)) == type(Nothing)


def test_compare():
    assert Nothing == Nothing
    for n in test_range:
        assert unit(n) != Nothing
        assert unit(n) is not Nothing


def test_ordering():
    assert (Nothing < Nothing) is False
    assert (Nothing > Nothing) is False
    for n in test_range:
        assert (Nothing > unit(n)) is False
        assert (unit(n) < Nothing) is False


def test_as_context_manager():
    for n in test_range:
        with pytest.raises(ExtractError):
            with unit(n) >> double >> fail >> double as result:
                assert False
                assert result

    with pytest.raises(ExtractError):
        with Nothing as n:
            assert False

    with pytest.raises(ExtractError):
        with double(n) as result:
            with Nothing as n:
                assert False

    with pytest.raises(ExtractError):
        with double(n) as result, Nothing as n:
            assert False


def test_bool():
    assert bool(Nothing) is False
    for n in test_range:
        assert bool(unit(n)) is True


def test_from_value():
    false_v = [False, None, 0, 0.0, (), [], {}, '', set(), frozenset()]
    for v in false_v:
        assert Maybe.from_value(v) is Nothing

    true_v = [True, 1, 1.0, (0,), [0], {0: 0}, '0', set('0'), frozenset('0')]
    for v in true_v:
        assert Maybe.from_value(v) == unit(v)


def test_as_iterator():
    for n in test_range:
        for i in unit(n):
            assert i == n

        assert list(unit(n)) == [n]


def test_bind():
    assert Nothing.bind(add_1) is Nothing
    for n in test_range:
        m = unit(n)
        assert m.bind(fail) is Nothing


def test_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> fail is Nothing
        assert fail(n) >> add_1 is Nothing


def test_reversed_bind_operator():
    for n in test_range:
        m = unit(n)
        assert fail << m is Nothing
        assert add_1 << fail(n) is Nothing


def test_chain_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> fail >> add_1 == Nothing
        assert m >> add_1 >> fail == Nothing
        assert m >> fail >> double == Nothing
        assert m >> double >> fail == Nothing


def test_monad_law_left_identity():
    for n in test_range:
        # unit n >>= f == f n
        f = fail
        assert unit(n) >> f == f(n)


def test_monad_law_right_identity():
    for n in test_range:
        # m >>= unit == m
        assert Nothing >> unit == Nothing


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


def test_maybe_decorator():
    @maybe
    def div(a, b):
        return a / b

    assert div(42, 21) == unit(2)
    assert div(42, 0) is Nothing


def test_maybe_decorator_with_predicate():
    @maybe(predicate=bool)
    def truth(x):
        return x

    assert truth(42) == unit(42)
    assert truth(None) is Nothing
    assert add_1(0) >> truth == unit(1)
    assert add_1(-1) >> truth is Nothing
    assert truth(False) >> double is Nothing
    assert double([]) >> truth is Nothing


def test_maybe_decorator_with_value():
    @maybe(nothing_on_value=None)
    def truth(x):
        return x

    assert truth(42) is not Nothing
    assert truth('') is not Nothing
    assert truth(0) is not Nothing
    assert truth(False) is not Nothing
    assert truth(None) is Nothing


def test_maybe_decorator_combined():
    @maybe(predicate=bool, nothing_on_value=42)
    def wrap(x):
        return x

    assert wrap(True) == unit(True)
    assert wrap(False) is Nothing
    assert wrap('something') == unit('something')
    assert wrap('') is Nothing
    assert wrap([False]) == unit([False])
    assert wrap([]) is Nothing
    assert wrap(1) == unit(1)
    assert wrap(0) is Nothing
    assert wrap(None) is Nothing
    assert wrap(42) is Nothing


def test_maybe_decorator_none_exception():
    @maybe(nothing_on_exception=None)
    def div(a, b):
        return a / b

    with pytest.raises(ZeroDivisionError):
        div(42, 0)


def test_maybe_decorator_empty_seq_exception():
    for empty in ([], tuple(), set()):
        @maybe(nothing_on_exception=empty)
        def div(a, b):
            return a / b

        with pytest.raises(ZeroDivisionError):
            div(42, 0)


def test_maybe_decorator_specific_exception():
    @maybe(nothing_on_exception=ZeroDivisionError)
    def div(a, b):
        return a / b

    assert div(42, 0) is Nothing


def test_maybe_decorator_specific_exception_tuple():
    @maybe(nothing_on_exception=(IOError, ZeroDivisionError))
    def div(a, b):
        if a < 0:
            raise IOError
        return a / b

    assert div(42, 0) is Nothing
    assert div(-42, 2) is Nothing


def test_first():
    assert first([Nothing, Just(42)]) == Just(42)
    assert first([Just(42), Just(43)]) == Just(42)
    assert first([Nothing, Nothing]) == Nothing
    assert first([]) == Nothing


def test_first_default():
    assert first([Nothing, Nothing], default=Just(42)) == Just(42)


def test_first_predicate():
    assert first([False, 0, 2, 1], predicate=bool) == Just(2)
    assert first([False, 0, ''], predicate=bool) == Nothing
    assert first(range(100), predicate=lambda x: x > 50) == Just(51)
    assert first(range(100), predicate=lambda x: x > 100) == Nothing


def test_first_wrap_just_only_if_not_already():
    assert first([False, True], predicate=bool) == Just(True)
    assert first([False, Just(True)], bool) != Just(Just(True))
    assert first([False, Just(True)], bool) == Just(True)


def test_first_is_lazy():
    def once():
        yield Just(42)
        raise Exception

    assert first(once()) == Just(42)
