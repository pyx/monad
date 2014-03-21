# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.monadplus - The MonadPlus Class."""

from . import Monad


class MonadPlus(Monad):
    """The MonadPlus Class.

    Monads that also support choice and failure.
    """
    # Associative Operator
    def __add__(self, monad):
        """The associative operator ``+``"""
        return self.plus(monad)

    # Associative Operation
    def plus(self, monad):
        """The Associative operation."""
        raise NotImplementedError

    #: The identity of ``plus``.
    #:
    #: This property should be a singleton, the following must be ``True``::
    #:
    #:    MP.zero is MP.zero
    #:
    #: It should satisfy the following law, left zero
    #: (notice the bind operator is haskell's ``>>=`` here)::
    #:
    #:    zero >>= f = zero
    zero = NotImplemented
