# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
from monad.types import Null


def test_null_repr():
    # for readability of autodoc-generated documents
    assert repr(Null) == 'Null'


def test_null_callable():
    assert Null() is Null
