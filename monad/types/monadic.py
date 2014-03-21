# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.monadic - The Monadic Fuction Wrapper."""

from . import Function


class Monadic(Function):
    """The Monadic Function Wrapper.

    Implements Kleisli composition operators ``>>`` and ``<<``.  It is
    equivalent to ``(>=>)`` and ``(<=<)`` in haskell.
    """
    # pylint: disable = too-few-public-methods
    def __lshift__(self, monad):
        return monad >> self

    def __rshift__(self, monadic):
        """Left-to-right Kleisli composition of monads. ``>>``"""
        if not callable(monadic):
            return NotImplemented
        # pylint: disable = star-args
        composed = lambda *args, **kwargs: self(*args, **kwargs) >> monadic
        return self.__class__(composed)
