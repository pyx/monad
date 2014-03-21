# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.applicative - The Applicative Functor Class."""

from . import Functor


class Applicative(Functor):
    """The Applicative Functor Class.

    Defines the following functions:

    - ``unit`` which act as constructor, it's called ``pure`` in some context.
    """
    # pylint: disable = abstract-method, too-few-public-methods
    #: The unit.
    #:
    #: Maps a value to a value in this type.
    #: Also called ``pure`` or ``return`` depends on context.
    unit = NotImplemented
