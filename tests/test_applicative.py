# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
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
    if 'applicative' in metafunc.funcargnames:
        metafunc.parametrize('applicative', testee, ids=ids)


def test_unit(applicative):
    unit = applicative.unit
    # const
    c = lambda _: 42
    # add_1
    a = 1 .__radd__
    # double
    d = 2 .__rmul__
    f = hash
    # identity
    i = lambda a: a
    for n in test_range:
        # unit . f = fmap f . unit
        assert unit(c(n)) == unit(n).fmap(c)
        assert unit(a(n)) == unit(n).fmap(a)
        assert unit(d(n)) == unit(n).fmap(d)
        assert unit(f(n)) == unit(n).fmap(f)
        assert unit(i(n)) == unit(n).fmap(i)
