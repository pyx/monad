# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.monad - The Monad Class."""

from . import Applicative
from ..utils import identity


class Unit(object):
    """Descriptor that always return the owner monad, used for ``unit``."""
    # pylint: disable = too-few-public-methods
    def __get__(self, instance, cls):
        """Returns the owner monad."""
        return cls


class Monad(Applicative):
    """The Monad Class.

    Implements bind operator ``>>`` and inverted bind operator ``<<`` as
    syntactic sugar.  It is equivalent to ``(>>=)`` and ``(=<<)`` in haskell,
    not to be confused with ``(>>)`` and ``(<<)`` in haskell.

    As python treats assignments as statements, there is no way we can
    overload ``>>=`` as a chainable bind, be it directly overloaded through
    ``__irshift__``, or derived by python itself through ``__rshift__``.

    The default implementations of ``bind``, ``fmap`` and ``join`` are mutual
    recursive, subclasses should at least either overload ``bind``, or
    ``fmap`` and ``join``, or all of them for better performance.
    """
    # Bind Operators
    def __rshift__(self, function):
        """The bind operator ``>>``"""
        if not callable(function):
            return NotImplemented
        return self.bind(function)

    def __rlshift__(self, function):
        """The inverted bind operator ``<<``"""
        if not callable(function):
            return NotImplemented
        return self.bind(function)

    def __repr__(self):
        return '{cls}({value})'.format(
            cls=type(self).__name__, value=repr(self.value))

    def bind(self, function):
        """The bind operation.

        ``function`` is a function that maps from the underlying value to a
        monadic type, something like signature ``f :: a -> M a`` in haskell's
        term.

        The default implementation defines ``bind`` in terms of ``fmap`` and
        ``join``.
        """
        return self.fmap(function).join()

    def fmap(self, function):
        """The fmap operation.

        The default implementation defines ``fmap`` in terms of ``bind`` and
        ``unit``.
        """
        # pylint: disable = star-args
        return self.bind(
            lambda *args, **kwargs: self.unit(function(*args, **kwargs))
        )

    def join(self):
        """The join operation.

        The default implementation defines ``join`` in terms of ``bind`` and
        ``identity`` function.
        """
        return self.bind(identity)

    #: The ``unit`` of monad.
    unit = Unit()
