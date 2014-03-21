# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.function - The Function Wrapper."""

from ..utils import compose


class Function(object):
    """The Function Wrapper.

    Support function composition via ``*`` operator.

    >>> add_1 = Function(lambda n: n + 1)
    >>> inc = add_1 * int
    >>> inc('42')
    43

    Support function piping via ``|`` operator.

    >>> inc2 = int | add_1 | add_1 | str
    >>> inc2('42')
    '44'
    """
    # pylint: disable = too-few-public-methods
    def __init__(self, callable_object):
        self.function = callable_object
        # just copy these, functools.wraps does too much
        for attr in ('__module__', '__name__', '__doc__'):
            setattr(self, attr, getattr(callable_object, attr, None))

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    def __mul__(self, other):
        return self.__class__(compose(self.function, other))

    def __ror__(self, other):
        return self.__mul__(other)

    def __rmul__(self, other):
        return self.__class__(compose(other, self.function))

    def __or__(self, other):
        return self.__rmul__(other)
