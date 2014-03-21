# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.list - The List Monad."""

from collections import Sequence
from itertools import chain

from . import LazySequence, MonadPlus
from ..mixins import Ord


class List(MonadPlus, Ord, Sequence):
    """The List Monad.

    Representing nondeterministic computation.

    >>> List(42)
    List(42)
    >>> List(1, 2, 3)
    List(1, 2, 3)
    >>> List([])
    List([])
    >>> List.from_iterable(range(3))
    List(0, 1, 2)
    >>> List.from_iterable(n for n in (1, 2, 3) if n % 2 == 0)
    List(2)
    >>> List(List(2))
    List(List(2))

    Lists are lazy

    >>> from itertools import count
    >>> m = List.from_iterable(count())
    >>> m[:5]
    List(0, 1, 2, 3, 4)
    >>> m[520:524]
    List(520, 521, 522, 523)
    >>> list(m[1000:1002])
    [1000, 1001]

    Bind operation with ``>>``

    >>> spawn = lambda cell: List(cell, cell)
    >>> spawn('c')
    List('c', 'c')
    >>> spawn('c') >> spawn
    List('c', 'c', 'c', 'c')
    >>> grow = lambda cell: List(cell + '~')
    >>> grow('o')
    List('o~')
    >>> grow('o') >> grow >> grow >> grow
    List('o~~~~')
    >>> generation = lambda cell: grow(cell) + spawn(cell)
    >>> first = List('o')
    >>> first
    List('o')
    >>> first >> generation
    List('o~', 'o', 'o')
    >>> first >> generation >> generation
    List('o~~', 'o~', 'o~', 'o~', 'o', 'o', 'o~', 'o', 'o')
    """
    # pylint: disable = too-many-ancestors
    def __init__(self, *items):
        super(List, self).__init__(LazySequence(items))

    def __getitem__(self, index):
        items = self.value.__getitem__(index)
        if isinstance(index, slice):
            return self.from_iterable(items)
        return items

    def __len__(self):
        return len(self.value)

    def __nonzero__(self):
        return len(self.value)

    def __repr__(self):
        """Customized Show."""
        return 'List({})'.format(', '.join(repr(x) for x in self))

    @classmethod
    def from_iterable(cls, iterator):
        """Creates ``List`` from iterable."""
        instance = cls.unit()
        instance.value = LazySequence(iterator)
        return instance

    def fmap(self, function):
        """fmap of List Monad."""
        return self.from_iterable(function(i) for i in self)

    def join(self):
        """join of List Monad."""
        return self.from_iterable(chain.from_iterable(self))

    def plus(self, monad):
        """plus operation, concatenates two ``List``."""
        if not isinstance(monad, type(self)):
            return NotImplemented
        return self.from_iterable(chain(self, monad))


List.zero = List()
