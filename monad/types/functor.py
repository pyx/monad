# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.functor - The Functor Class."""


class Functor(object):
    """The Functor Class.

    Defines function ``fmap``, and should satisfy these laws::

        fmap id  ==  id
        fmap (f . g)  ==  fmap f . fmap g
    """
    # pylint: disable = too-few-public-methods
    def __init__(self, value):
        self.value = value

    def fmap(self, function):
        """The fmap operation."""
        raise NotImplementedError
