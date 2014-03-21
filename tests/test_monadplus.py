# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.types import MonadPlus
from monad.types import Maybe
from monad.types import List

testee = [
    Maybe,
    List,
]
test_range = range(-100, 100)
ids = [t.__name__ for t in testee]


def pytest_generate_tests(metafunc):
    if 'monadplus' in metafunc.funcargnames:
        metafunc.parametrize('monadplus', testee, ids=ids)


def test_monadplus_is_abstract():
    with pytest.raises(NotImplementedError):
        MonadPlus(1).plus(1)


# Note:
# As stated on haskell wiki: http://www.haskell.org/haskellwiki/MonadPlus
# The precise set of rules that MonadPlus should obey is not agreed upon.
# More discussion here:
# http://www.haskell.org/haskellwiki/MonadPlus_reform_proposal
# This is my own interpretation, especially the implementation of Maybe Monad
# has unbiased plus, which satisfy Monoid and *Left Distribution*.

def test_zero_implemented(monadplus):
    zero = monadplus.zero
    assert zero is monadplus.zero


def test_plus_implemented(monadplus):
    zero = monadplus.zero
    assert zero.plus(zero) == zero


def test_plus_operator(monadplus):
    unit = monadplus.unit
    for n in test_range:
        m = unit(n)
        assert m + unit(n) == m.plus(unit(n))


def test_plus_zero_form_a_monoid(monadplus):
    unit = monadplus.unit
    zero = monadplus.zero
    for n in test_range:
        m = unit(n)
        # zero is a neutral element
        # zero + m = m
        assert zero + m == m
        assert zero.plus(m) == m
        # m + zero = m
        assert m + zero == m
        assert m.plus(zero) == m


def test_left_zero(monadplus):
    unit = monadplus.unit
    zero = monadplus.zero
    f = lambda n: unit(n + 1)

    # zero >>= f = zero
    assert zero >> f == zero

    # v >> zero = zero
    # Not testing this since the >> we implemented is actually >>= in
    # haskell, if we really want to do it, here is how:
    # for n in test_range:
    #     bind_and_discard = lambda m, other_m: other_m
    #     v = unit(n)
    #     assert bind_and_discard(v, zero) == zero


def test_left_distribution(monadplus):
    unit = monadplus.unit
    k = lambda n: unit(n + 1)
    # (m `mplus` n) >>= k  =  (m >>= k) `mplus` (n >>= k)
    for a in test_range:
        m = unit(a)
        n = unit(a * 2)
        assert (m + n) >> k == (m >> k) + (n >> k)
