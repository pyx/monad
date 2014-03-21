# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.decorators import monadic
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


def test_monadic_kleisli_composition_operator_type_check():
    with pytest.raises(TypeError):
        monadic(lambda a: a) >> 1


def test_left_to_right_kleisli_composition(monad):
    unit = monad.unit
    add_1 = monadic(lambda n: unit(n + 1))
    double = monadic(lambda n: unit(n * 2))
    action = add_1 >> double
    for n in test_range:
        m = unit(n)
        assert m >> action == m >> add_1 >> double


def test_right_to_left_kleisli_composition(monad):
    unit = monad.unit
    add_1 = monadic(lambda n: unit(n + 1))
    double = monadic(lambda n: unit(n * 2))
    action = double << add_1
    for n in test_range:
        m = unit(n)
        assert m >> action == m >> add_1 >> double


def test_chain_right_to_left_kleisli_composition(monad):
    unit = monad.unit
    add_1 = monadic(lambda n: unit(n + 1))
    double = monadic(lambda n: unit(n * 2))
    for n in test_range:
        m = unit(n)
        assert add_1 << add_1 << m == m >> add_1 >> add_1
        assert double << double << m == m >> double >> double
        assert add_1 << double << m == m >> double >> add_1
        assert double << add_1 << m == m >> add_1 >> double
