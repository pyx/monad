# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.actions - useful monadic actions."""

from .decorators import function, monadic


@function
def tryout(*functions):
    """Combine functions into one.

    Returns a monadic function that when called, will try out functions in
    ``functions`` one by one in order, testing the result, stop and return
    with the first value that is true or the last result.

    >>> zero = lambda n: 'zero' if n == 0 else False
    >>> odd = lambda n: 'odd' if n % 2 else False
    >>> even = lambda n: 'even' if n % 2 == 0 else False
    >>> test = tryout(zero, odd, even)
    >>> test(0)
    'zero'
    >>> test(1)
    'odd'
    >>> test(2)
    'even'
    """
    @monadic
    def trying(*args, **kwargs):
        """Monadic function that try out functions in order."""
        last = None
        for func in functions:
            last = func(*args, **kwargs)
            if last:
                break
        return last
    return trying


# As decorators function and monadic turn decorated functions into Function
# and Monadic instance objects, respectively, doctest will ignore docstring in
# them, the following adds those docstring into testsuite back again,
# explicitly.
__test__ = {
    'tryout': tryout.__doc__,
}
