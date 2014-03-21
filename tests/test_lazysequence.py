# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
from itertools import count

import pytest

from monad.types import LazySequence


def test_lazy_sequence_initialization():
    # no need to use assert here, if LazySequence is not lazy, execution will
    # never stop in for statement.
    infinite = LazySequence(count())
    for n in infinite:
        if n == 42:
            break


def test_lazy_sequence_iterator():
    numbers = LazySequence(n for n in range(10))

    iter1 = iter(numbers)
    iter2 = iter(numbers)

    for index, (i1, i2) in enumerate(zip(iter1, iter2)):
        assert index == i1 == i2


def test_lazy_sequence_eq():
    seq = LazySequence([1, 2])

    assert seq == seq
    assert seq == LazySequence([1, 2])

    not_seq = object()
    assert (seq == not_seq) is False


def test_lazy_sequence_ording():
    seq = LazySequence([1, 2])
    assert (seq < seq) is False

    class NotSeq:
        pass

    with pytest.raises(TypeError):
        seq < NotSeq()
