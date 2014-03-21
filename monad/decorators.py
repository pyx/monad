# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.decorators - helpful decorators."""

from .types import Function


def function(callable_object):
    """Decorator that wraps a callabe into :class:`Function`.

    >>> to_int = function(int)
    >>> to_int('42')
    42
    >>> @function
    ... def puts(msg, times=1):
    ...     while times > 0:
    ...         print(msg)
    ...         times -= 1
    >>> puts('Hello, world', 2)
    Hello, world
    Hello, world
    """
    return Function(callable_object)
