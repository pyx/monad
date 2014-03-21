# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.identity - The Identity Monad."""

from . import Monad
from ..mixins import ContextManager, Ord


class Identity(Monad, ContextManager, Ord):
    """The Identity Monad.

    >>> Identity(42)
    Identity(42)
    >>> Identity([1, 2, 3])
    Identity([1, 2, 3])

    Comparison with ``==``, as long as what's wrapped inside are comparable.

    >>> Identity(42) == Identity(42)
    True
    >>> Identity(42) == Identity(24)
    False
    """
    def bind(self, function):
        return function(self.value)
