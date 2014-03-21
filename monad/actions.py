# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.actions - useful monadic actions."""

from .decorators import function, monadic
from .types import Either, Left, Right
from .types import Just, Nothing
from .utils import identity


@function
def either(left_handler, right_handler=identity):
    """Case analysis for ``Either``.

    Returns a function that when called with a value of type ``Either``,
    applies either ``left_handler`` or ``right_handler`` to that value
    depending on the type of it.  If an incompatible value is passed, a
    ``TypeError`` will be raised.

    >>> def log(v):
    ...     print('Got Left({})'.format(v))
    >>> logger = either(left_handler=log)
    >>> logger(Left(1))
    Got Left(1)
    >>> logger(Right(1))
    1
    >>> def inc(v):
    ...     return v + 1
    >>> act = either(log, inc)
    >>> [act(v) for v in (Left(0), Right(1), Left(2), Right(3))]
    Got Left(0)
    Got Left(2)
    [None, 2, None, 4]
    """
    @function
    def analysis(an_either):
        """Apply handler functions based on value."""
        aug_type = type(an_either)
        if not issubclass(aug_type, Either):
            raise TypeError(
                'applied either on incompatible type: %s' % aug_type)
        if issubclass(aug_type, Left):
            return left_handler(an_either.value)
        assert issubclass(aug_type, Right)
        return right_handler(an_either.value)
    return analysis


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


@monadic
def first(sequence, default=Nothing, predicate=None):
    """Iterate over a sequence, return the first ``Just``.

    If ``predicate`` is provided, ``first`` returns the first item that
    satisfy the ``predicate``, the item will be wrapped in a :class:`Just` if
    it is not already, so that the return value of this function will be an
    instance of :class:`Maybe` in all circumstances.
    Returns ``default`` if no satisfied value in the sequence, ``default``
    defaults to :data:`Nothing`.

    >>> from monad.types import Just, Nothing
    >>> first([Nothing, Nothing, Just(42), Nothing])
    Just(42)
    >>> first([Just(42), Just(43)])
    Just(42)
    >>> first([Nothing, Nothing, Nothing])
    Nothing
    >>> first([])
    Nothing
    >>> first([Nothing, Nothing], default=Just(2))
    Just(2)
    >>> first([False, 0, True], predicate=bool)
    Just(True)
    >>> first([False, 0, Just(1)], predicate=bool)
    Just(1)
    >>> first([False, 0, ''], predicate=bool)
    Nothing
    >>> first(range(100), predicate=lambda x: x > 40 and x % 2 == 0)
    Just(42)
    >>> first(range(100), predicate=lambda x: x > 100)
    Nothing

    This is basically a customized version of ``msum`` for :class:`Maybe`,
    a separate function like this is needed because there is no way to write a
    generic ``msum`` in python that cab be evaluated in a non-strict way.
    The obvious ``reduce(operator.add, sequence)``, albeit beautiful, is
    strict, unless we build up the sequence with generator expressions
    in-place.

    Maybe (pun intended!) implemented as ``MonadOr`` instead of ``MonadPlus``
    might be more semantically correct in this case.
    """
    if predicate is None:
        predicate = lambda m: m and isinstance(m, Just)

    for item in sequence:
        if predicate(item):
            if not isinstance(item, Just):
                item = Just(item)
            return item
    return default


# As decorators function and monadic turn decorated functions into Function
# and Monadic instance objects, respectively, doctest will ignore docstring in
# them, the following adds those docstring into testsuite back again,
# explicitly.
__test__ = {
    'either': either.__doc__,
    'tryout': tryout.__doc__,
    'first': first.__doc__,
}
