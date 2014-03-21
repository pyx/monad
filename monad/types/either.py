# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.either - The Either Monad."""

from . import Monad, Monadic
from ..mixins import ContextManager, Ord


class Either(Monad, ContextManager, Ord):
    """The Either Monad.

    Represents values/computations with two possibilities.

    >>> Right(42)
    Right(42)
    >>> Right([1, 2, 3])
    Right([1, 2, 3])
    >>> Left('Error')
    Left('Error')
    >>> Right(Left('Error'))
    Right(Left('Error'))
    >>> isinstance(Right(1), Either)
    True
    >>> isinstance(Left(None), Either)
    True
    >>> saving = 100
    >>> broke = Left('I am broke')
    >>> spend = lambda cost: broke if cost > saving else Right(saving - cost)
    >>> spend(90)
    Right(10)
    >>> spend(120)
    Left('I am broke')
    >>> safe_div = lambda a, b: Left(str(a) + '/0') if b == 0 else Right(a / b)
    >>> safe_div(12.0, 6)
    Right(2.0)
    >>> safe_div(12.0, 0)
    Left('12.0/0')

    Bind operation with ``>>``

    >>> inc = lambda n: Right(n + 1) if type(n) is int else Left('Type error')
    >>> Right(0)
    Right(0)
    >>> Right(0) >> inc
    Right(1)
    >>> Right(0) >> inc >> inc
    Right(2)
    >>> Right('zero') >> inc
    Left('Type error')

    Comparison with ``==``, as long as they are the same type and what's
    wrapped inside are comparable.

    >>> Left(42) == Left(42)
    True
    >>> Right(42) == Right(42)
    True
    >>> Left(42) == Right(42)
    False

    A :py:class:`Left` is less than a :py:class:`Right`, or compare the two by
    the values inside if thay are of the same type.

    >>> Left(42) < Right(42)
    True
    >>> Right(0) > Left(100)
    True
    >>> Left('Error message') > Right(42)
    False
    >>> Left(100) > Left(42)
    True
    >>> Right(-2) < Right(-1)
    True
    """
    def __init__(self, value):
        super(Either, self).__init__(value)
        if type(self) is Either:
            raise NotImplementedError('Please use Left or Right instead')

    def bind(self, function):
        """The bind operation of :py:class:`Either`.

        Applies function to the value if and only if this is a
        :py:class:`Right`.
        """
        return self and function(self.value)

    def __repr__(self):
        """Customize Show."""
        fmt = 'Right({})' if self else 'Left({})'
        return fmt.format(repr(self.value))

    # Customize Ord logic
    def __lt__(self, monad):
        """Override to handle special case: Right."""
        if not isinstance(monad, (Left, Right)):
            fmt = "unorderable types: {} and {}'".format
            raise TypeError(fmt(type(self), type(monad)))
        if type(self) is type(monad):
            # same type, either both lefts or rights, compare against value
            return self.value < monad.value
        if monad:
            # self is Left and monad is Right, left is less than right
            return True
        else:
            return False


class Left(Either):
    """Left of :py:class:`Either`."""
    def __bool__(self):
        # pylint: disable = no-self-use
        return False
    __nonzero__ = __bool__


class Right(Either):
    """Right of :py:class:`Either`."""


Either.unit = Monadic(Right)
