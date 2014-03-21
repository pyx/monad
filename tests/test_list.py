# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.decorators import producer
from monad.types import List

test_range = range(-100, 100)
unit = List.unit
zero = List.zero


def add_1(n):
    return unit(n + 1)


def double(n):
    return unit(n, n)


def empty(n):
    return zero


def test_compare():
    assert zero == List()


def test_ording():
    for n in test_range:
        assert zero < List(n)


def test_bool():
    assert bool(zero) is False
    for n in test_range:
        assert bool(unit(n)) is True


def test_from_iterable():
    fi = List.from_iterable
    assert fi(range(3)) == unit(0, 1, 2)
    assert fi([3, 2, 1]) == unit(3, 2, 1)
    assert fi(n for n in [3, 5, 8]) == unit(3, 5, 8)


def test_len():
    for n in range(100):
        m = List.from_iterable(range(n))
        assert len(m) == n


def test_getitem():
    rg = range(100)
    m = List.from_iterable(rg)
    for n in rg:
        assert m[n] == n


def test_bind():
    for n in test_range:
        m = unit(n)
        assert m.bind(add_1) == unit(n + 1)
        assert m.bind(double) == unit(n, n)
        assert add_1(n).bind(double) == unit((n + 1), (n + 1))

        assert m.bind(add_1).bind(empty) == zero
        assert zero.bind(add_1) == zero
        assert m.bind(double).bind(empty) == zero
        assert zero.bind(double) == zero


def test_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> add_1 == unit(n + 1)
        assert m >> double == unit(n, n)
        assert add_1(n) >> double == unit((n + 1), (n + 1))

        assert zero >> add_1 == zero
        assert zero >> double == zero
        assert m >> empty == zero


def test_reversed_bind_operator():
    for n in test_range:
        m = unit(n)
        assert add_1 << m == m >> add_1
        assert double << m == m >> double
        assert double << add_1(n) == add_1(n) >> double

        assert add_1 << zero == zero >> add_1
        assert double << zero == zero >> double
        assert empty << m == m >> empty


def test_chain_bind_operator():
    for n in test_range:
        m = unit(n)
        assert m >> add_1 >> add_1 == unit(n + 1 + 1)
        assert m >> double >> double == unit(n, n, n, n)
        assert m >> add_1 >> double == unit(n + 1, n + 1)
        assert m >> double >> add_1 == unit(n + 1, n + 1)
        assert m >> add_1 >> empty == zero
        assert m >> double >> empty == zero
        assert m >> empty >> add_1 == zero
        assert m >> empty >> double == zero


def test_monad_law_left_identity():
    for n in test_range:
        # unit n >>= f == f n
        f = unit
        assert unit(n) >> f == f(n)
        f = add_1
        assert unit(n) >> f == f(n)
        f = double
        assert unit(n) >> f == f(n)
        f = empty
        assert unit(n) >> f == f(n)


def test_monad_law_right_identity():
    for n in test_range:
        # m >>= unit == m
        m = unit(n)
        assert m >> unit == m
        m = add_1(n)
        assert m >> unit == m
        m = double(n)
        assert m >> unit == m
        m = empty(n)
        assert m >> unit == m


def test_monad_law_associativity():
    for n in test_range:
        # m >>= (\x -> k x >>= h)  ==  (m >>= k) >>= h
        m = unit(n)
        k = add_1
        h = double
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = add_1
        h = empty
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = empty
        h = double
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = empty
        h = empty
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h


def test_plus_type_check():
    assert unit(1).plus(1) == NotImplemented
    with pytest.raises(TypeError):
        unit(1) + 1


def test_list_is_lazy():
    from itertools import count
    # no need to use assert here, if LazySequence is not lazy, execution will
    # never stop in for statement.
    infinite = List.from_iterable(count())
    for n in infinite:
        if n == 42:
            break

    def never_stop(n):
        return infinite

    # this is okay because zero binds something yields zero immediately
    # without evaluating that something.
    assert zero >> never_stop >> double == zero


def test_list_comprehension():
    a = [n for o in unit(1, 2, 3) for m in double(o) for n in add_1(m)]
    assert a == [2, 2, 3, 3, 4, 4]
    a = [n for o in unit(1, 2, 3) for m in empty(o) for n in add_1(m)]
    assert a == []


def test_producer_decorator():
    @producer
    def range_iter():
        return test_range

    for m, n in zip(range_iter(), test_range):
        assert m == n

    @producer
    def list_iter():
        return list(test_range)

    for m, n in zip(list_iter(), test_range):
        assert m == n

    @producer
    def generator():
        yield 1
        yield 2
        yield 3

    assert generator() == List(1, 2, 3)


def test_producer_empty_on_exception():
    class Error(Exception):
        pass

    @producer(empty_on_exception=None)
    def fail():
        raise Error

    with pytest.raises(Error):
        fail()

    @producer(empty_on_exception=Error)
    def empty():
        raise Error

    assert empty() == unit()
