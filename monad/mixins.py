# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.mixins - implements common mixin classes."""

from functools import total_ordering

from .exceptions import ExtractError
from .utils import identity


class ContextManager(object):
    """Mixin class that support ``with`` statement for monad."""
    # pylint: disable = too-few-public-methods
    def __enter__(self):
        if not self:
            raise ExtractError(self)
        return self.bind(identity)

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

    bind = NotImplemented


@total_ordering
class Ord(object):
    """Mixin class that implements rich comparison ordering methods."""
    # pylint: disable = too-few-public-methods
    def __eq__(self, other):
        if self is other:
            return True
        elif not isinstance(other, type(self)):
            return NotImplemented
        else:
            return self.value == other.value

    def __lt__(self, other):
        if self is other:
            return False
        elif isinstance(other, type(self)):
            return self.value < other.value
        else:
            fmt = "unorderable types: {} and {}'".format
            raise TypeError(fmt(type(self), type(other)))

    value = NotImplemented
