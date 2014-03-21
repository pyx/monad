# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.maybe - The Maybe Monad."""

from . import MonadPlus, Null
from ..mixins import ContextManager, Ord


class Maybe(MonadPlus, ContextManager, Ord):
    """The Maybe Monad.

    Representing values/computations that may fail.

    >>> Just(42)
    Just(42)
    >>> Just([1, 2, 3])
    Just([1, 2, 3])
    >>> Just(Nothing)
    Just(Nothing)
    >>> Just(Just(2))
    Just(Just(2))
    >>> isinstance(Just(1), Maybe)
    True
    >>> isinstance(Nothing, Maybe)
    True
    >>> saving = 100
    >>> spend = lambda cost: Nothing if cost > saving else Just(saving - cost)
    >>> spend(90)
    Just(10)
    >>> spend(120)
    Nothing
    >>> safe_div = lambda a, b: Nothing if b == 0 else Just(a / b)
    >>> safe_div(12.0, 6)
    Just(2.0)
    >>> safe_div(12.0, 0)
    Nothing

    Bind operation with ``>>``

    >>> inc = lambda n: Just(n + 1) if isinstance(n, int) else Nothing
    >>> Just(0)
    Just(0)
    >>> Just(0) >> inc
    Just(1)
    >>> Just(0) >> inc >> inc
    Just(2)
    >>> Just('zero') >> inc
    Nothing

    Comparison with ``==``, as long as what's wrapped inside are comparable.

    >>> Just(42) == Just(42)
    True
    >>> Just(42) == Nothing
    False
    >>> Nothing == Nothing
    True
    """
    @classmethod
    def from_value(cls, value):
        """Wraps ``value`` in a :class:`Maybe` monad.

        Returns a :class:`Just` if the value is evaluated as true.
        :data:`Nothing` otherwise.
        """
        return cls.unit(value) if value else Nothing

    def bind(self, function):
        """The bind operation of :class:`Maybe`.

        Applies function to the value if and only if this is a :class:`Just`.
        """
        return Nothing if self is Nothing else function(self.value)

    def __bool__(self):
        return self is not Nothing
    __nonzero__ = __bool__

    def __repr__(self):
        """Customized Show."""
        if self is Nothing:
            return 'Nothing'
        else:
            return 'Just({})'.format(repr(self.value))

    def __iter__(self):
        if self is not Nothing:
            yield self.value

    # Customized Ord logic
    def __lt__(self, monad):
        """Override to handle special case: Nothing."""
        if self is Nothing and monad is Nothing:
            return False
        elif self is Nothing:
            # Nothing is less than something.
            return True
        elif monad is Nothing:
            # self is not Nothing and monad is Nothing here
            return False
        else:
            # Test normally
            return super(Maybe, self).__lt__(monad)

    # MonadPlus operation
    def plus(self, monad):
        return self or monad


# pylint: disable = invalid-name
Just = Maybe
#: The :class:`Maybe` that represents nothing, a singleton, like ``None``.
Nothing = Maybe(Null)
Maybe.zero = Nothing
# pylint: enable = invalid-name
