# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
from monad.types import Identity
from monad.types import Maybe
from monad.types import Either

testee = [
    Identity,
    Maybe,
    Either,
]
test_range = range(-100, 100)
ids = [t.__name__ for t in testee]


def pytest_generate_tests(metafunc):
    if 'monad' in metafunc.funcargnames:
        metafunc.parametrize('monad', testee, ids=ids)


def test_as_context_manager(monad):
    unit = monad.unit
    add_1 = lambda n: unit(n + 1)
    double = lambda n: unit(n * 2)
    for n in test_range:
        with unit(n) as num:
            with add_1(num) as n_1:
                with double(n_1) as result:
                    assert result == (n + 1) * 2

    for n in test_range:
        with unit(n) as num, double(num) as n2, add_1(n2) as result:
            assert result == n * 2 + 1

    for n in test_range:
        with unit(n) >> double >> add_1 >> double as result:
            assert result == (n * 2 + 1) * 2
