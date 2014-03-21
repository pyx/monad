# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
from monad.types import Function
from monad.decorators import function


def test_callable():
    to_int = Function(int)
    assert to_int('42') == 42
    to_int = Function(lambda n: int(n))
    assert to_int('42') == 42

    class ToInt(object):
        def __call__(self, n):
            return int(n)

    to_int = Function(ToInt())
    assert to_int('42') == 42


def test_composition_operator():
    to_int = Function(int)
    add_1 = Function(lambda n: n + 1)
    to_s = Function(str)

    inc = add_1 * to_int
    assert inc('42') == add_1(to_int('42'))

    inc_s = to_s * add_1 * to_int
    assert inc_s('42') == to_s(add_1(to_int('42')))


def test_pipe_operator():
    to_int = Function(int)
    add_1 = Function(lambda n: n + 1)
    to_s = Function(str)

    inc = to_int | add_1
    assert inc('42') == add_1(to_int('42'))

    inc_s = to_int | add_1 | to_s
    assert inc_s('42') == to_s(add_1(to_int('42')))


def test_composition_auto_promote():
    add_1 = Function(lambda n: n + 1)

    inc = add_1 * int
    assert inc('42') == 43
    inc = int | add_1
    assert inc('42') == 43

    inc_s = str * add_1
    assert inc_s(42) == '43'
    inc_s = add_1 | str
    assert inc_s(42) == '43'


def test_composition_pipe_equivalent():
    add_1 = Function(lambda n: n + 1)
    assert (add_1 * int)('42') == (int | add_1)('42')


def test_compose():
    identity = lambda a: a
    # Left identity
    f = Function(int)
    g = identity * f

    assert f('42') == g('42')

    for n in range(42):  # this number is not significant here.
        assert f(n) == g(n)

    # Right identity
    f = Function(str)
    g = f * identity

    assert f(42) == g(42)

    for n in range(42):  # this number is not significant here.
        assert f(n) == g(n)

    # Associative

    # NOTE: these functions are specifically chosen, so that when composed in
    # different orders, yield different outputs.
    f = Function(hash)
    g = Function(str)
    h = Function(type)

    f1 = f * (g * h)
    f2 = (f * g) * h

    ns = [42, 0.5, '42', sum, f, lambda: 0]
    for n in ns:
        # make sure these functions yield different outputs when composed in
        # different order,
        assert f1(n) != (f * (h * g))(n)
        assert f2(n) != (f * (h * g))(n)
        assert f1(n) != (g * (f * h))(n)
        assert f2(n) != (g * (f * h))(n)
        assert f1(n) != (g * (h * f))(n)
        assert f2(n) != (g * (h * f))(n)
        assert f1(n) != (h * (g * f))(n)
        assert f2(n) != (h * (g * f))(n)
        assert f1(n) != (h * (f * g))(n)
        assert f2(n) != (h * (f * g))(n)
        # but compose should obey associative law.
        assert f1(n) == f2(n)


def test_decorator():
    @function
    def to_int(n):
        return int(n)

    assert to_int('42') == 42
