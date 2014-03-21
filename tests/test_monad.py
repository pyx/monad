# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.types import Identity
from monad.types import Maybe
from monad.types import Either
from monad.types import List

testee = [
    Identity,
    Maybe,
    Either,
    List,
]
test_range = range(-100, 100)
ids = [t.__name__ for t in testee]


def pytest_generate_tests(metafunc):
    if 'monad' in metafunc.funcargnames:
        metafunc.parametrize('monad', testee, ids=ids)


def test_unit(monad):
    for n in test_range:
        # unit should act as a contructor
        assert isinstance(monad.unit(n), monad)


def test_join(monad):
    unit = monad.unit
    for n in test_range:
        # join should remove one level of monadic structure
        # m m a -> m a
        m = unit(n)
        assert unit(m).join() == m


def test_bind(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        m = unit(n)
        assert m.bind(add_1) == unit(n + 1)
        assert m.bind(double) == unit(n * 2)
        assert add_1(n).bind(double) == unit((n + 1) * 2)


def test_bind_operator(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        m = unit(n)
        assert m >> add_1 == unit(n + 1)
        assert m >> double == unit(n * 2)
        assert add_1(n) >> double == unit((n + 1) * 2)


def test_bind_operator_type_check(monad):
    unit = monad.unit
    non_callable = object()
    with pytest.raises(TypeError):
        unit(1) >> non_callable


def test_reversed_bind_operator(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        m = unit(n)
        assert add_1 << m == m >> add_1
        assert double << m == m >> double
        assert double << add_1(n) == add_1(n) >> double


def test_reversed_bind_operator_type_check(monad):
    unit = monad.unit
    non_callable = object()
    with pytest.raises(TypeError):
        non_callable << unit(1)


def test_chain_bind_operator(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        m = unit(n)
        assert m >> add_1 >> add_1 == unit(n + 1 + 1)
        assert m >> double >> double == unit(n * 2 * 2)
        assert m >> add_1 >> double == unit((n + 1) * 2)
        assert m >> double >> add_1 == unit(n * 2 + 1)


def test_chain_reversed_bind_operator(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        m = unit(n)
        # NOTE: because there is no way to redefine the evaluation direction
        # of operators in python, parentheses are needed, to test the chain
        # action of reversed bind operator.
        assert add_1 << (add_1 << m) == m >> add_1 >> add_1
        assert double << (double << m) == m >> double >> double
        assert add_1 << (double << m) == m >> double >> add_1
        assert double << (add_1 << m) == m >> add_1 >> double


def test_monad_law_left_identity(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        # unit n >>= f == f n
        f = unit
        assert unit(n) >> f == f(n)
        f = add_1
        assert unit(n) >> f == f(n)
        f = double
        assert unit(n) >> f == f(n)


def test_monad_law_right_identity(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        # m >>= unit == m
        m = unit(n)
        assert m >> unit == m
        m = add_1(n)
        assert m >> unit == m
        m = double(n)
        assert m >> unit == m


def test_monad_law_associativity(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        # m >>= (\x -> k x >>= h)  ==  (m >>= k) >>= h
        m = unit(n)
        k = add_1
        h = double
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
        k = lambda a: unit(str(a))
        h = lambda a: unit(hash(a))
        assert m >> (lambda x: k(x) >> h) == (m >> k) >> h
