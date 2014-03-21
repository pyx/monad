# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.mixins import Ord
from monad.types import Identity
from monad.types import Maybe
from monad.types import Left, Right
from monad.types import List

testee = [
    Identity,
    Maybe,
    Left,
    Right,
    List,
]
test_range = range(-100, 100)
ids = [t.__name__ for t in testee]


def pytest_generate_tests(metafunc):
    if 'cls' in metafunc.funcargnames:
        metafunc.parametrize('cls', testee, ids=ids)


def test_ord_is_abstract():
    with pytest.raises(TypeError):
        Ord() < None


def test_compare(cls):
    for n in test_range:
        assert cls(n) == cls(n)
        assert cls(n) != cls(n + 1)


def test_ordering(cls):
    for n in test_range:
        assert (cls(n) < cls(n)) is False
        assert (cls(n) > cls(n)) is False
        m = cls(n)
        assert (m < m) is False
        assert (m > m) is False
        assert cls(n) < cls(n + 1)
        assert cls(n) > cls(n - 1)
