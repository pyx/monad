# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
import pytest

from monad.utils import compose, identity, suppress


def test_compose():
    # Left identity
    f = int
    g = compose(identity, f)

    assert f('42') == g('42')

    for n in range(42):  # this number is not significant here.
        assert f(n) == g(n)

    # Right identity
    f = str
    g = compose(f, identity)

    assert f(42) == g(42)

    for n in range(42):  # this number is not significant here.
        assert f(n) == g(n)

    # Associative

    # NOTE: these functions are specifically chosen, so that when composed in
    # different orders, yield different outputs.
    f = hash
    g = str
    h = type

    f1 = compose(f, compose(g, h))
    f2 = compose(compose(f, g), h)

    ns = [42, 0.5, '42', sum, f, lambda: 0]
    for n in ns:
        # make sure these functions yield different outputs when composed in
        # different order,
        assert f1(n) != compose(f, compose(h, g))(n)
        assert f2(n) != compose(f, compose(h, g))(n)
        assert f1(n) != compose(g, compose(f, h))(n)
        assert f2(n) != compose(g, compose(f, h))(n)
        assert f1(n) != compose(g, compose(h, f))(n)
        assert f2(n) != compose(g, compose(h, f))(n)
        assert f1(n) != compose(h, compose(g, f))(n)
        assert f2(n) != compose(h, compose(g, f))(n)
        assert f1(n) != compose(h, compose(f, g))(n)
        assert f2(n) != compose(h, compose(f, g))(n)
        # but compose should obey associative law.
        assert f1(n) == f2(n)


def test_identity():
    for n in [0, 1, 'a', [], {}, None, True, False, map, IOError, identity]:
        assert identity(n) is n


def test_suppress():
    class TestException(Exception):
        pass

    def fail():
        raise TestException

    with pytest.raises(TypeError):
        with suppress('Not an exception'):
            assert False  # should not reach here

    with pytest.raises(TestException):
        fail()

    with suppress(TestException):
        fail()

    with suppress(ZeroDivisionError):
        42 / 0

    with pytest.raises(TestException):
        with suppress(ZeroDivisionError):
            fail()

    with suppress(ZeroDivisionError, TestException):
        fail()
        42 / 0
