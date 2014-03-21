# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.lazysequence - a sequence type with lazy evaluation."""

from collections import Sequence
from functools import total_ordering
from itertools import islice

from ..utils import suppress


@total_ordering
class LazySequence(Sequence):
    """Sequence with lazy evaluation.

    >>> from itertools import count
    >>> seq = LazySequence(count())
    >>> seq[1]
    1
    >>> list(seq[3:5])
    [3, 4]
    >>> list(seq[:20:2])
    [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
    """
    def __init__(self, iterable):
        self.iterable = iter(iterable)
        self.items = []

    def __getitem__(self, index):
        if isinstance(index, slice):
            iterable = islice(self, index.start, index.stop, index.step)
            return self.__class__(iterable)

        if self.iterable is None:
            # that's all we have
            return self.items[index]

        item_numbers = len(self.items)
        finished = object()

        # get until enough
        while index < 0 or index >= item_numbers:
            next_item = next(self.iterable, finished)
            if next_item is finished:
                self.iterable = None
                break
            self.items.append(next_item)
            item_numbers += 1

        return self.items[index]

    def __len__(self):
        return len(self.strict.items)

    def __eq__(self, other):
        if self is other:
            return True
        elif isinstance(other, type(self)):
            return self.strict.items == other.strict.items
        else:
            return NotImplemented

    def __lt__(self, other):
        if self is other:
            return False
        elif isinstance(other, type(self)):
            return self.strict.items < other.strict.items
        else:
            fmt = "unorderable types: {} and {}'".format
            raise TypeError(fmt(type(self), type(other)))

    @property
    def strict(self):
        """Proxy to self that forces evaluation when accessed."""
        if self.iterable is not None:
            # force consume all items from self.iterable first
            with suppress(IndexError):
                id(self[-1])
        return self
