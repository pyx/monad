===================================
monad - a functional python package
===================================


Introduction
============


What?
-----

Monads in python, with some helpful functions.


How?
----

::

  >>> from monad.decorators import maybe
  >>> parse_int = maybe(int)
  >>> parse_int(42)
  Just(42)
  >>> parse_int('42')
  Just(42)
  >>> parse_int('42.2')
  Nothing

  >>> parse_float = maybe(float)
  >>> parse_float('42.2')
  Just(42.2)

  >>> from monad.actions import tryout
  >>> parse_number = tryout(parse_int, parse_float)
  >>> tokens = [2, '0', '4', 'eight', '10.0']
  >>> [parse_number(token) for token in tokens]
  [Just(2), Just(0), Just(4), Nothing, Just(10.0)]

  >>> @maybe
  ... def reciprocal(n):
  ...     return 1. / n
  >>> reciprocal(2)
  Just(0.5)
  >>> reciprocal(0)
  Nothing

  >>> process = parse_number >> reciprocal
  >>> process('4')
  Just(0.25)
  >>> process('0')
  Nothing
  >>> [process(token) for token in tokens]
  [Just(0.5), Nothing, Just(0.25), Nothing, Just(0.1)]
  >>> [parse_number(token) >> reciprocal for token in tokens]
  [Just(0.5), Nothing, Just(0.25), Nothing, Just(0.1)]
  >>> [parse_number(token) >> reciprocal >> reciprocal for token in tokens]
  [Just(2.0), Nothing, Just(4.0), Nothing, Just(10.0)]


Why?
----

Why not.


Requirements
============

- CPython >= 2.7


Installation
============

Install from PyPI::

  pip install monad

Install from source, download source package, decompress, then ``cd`` into source directory, run::

  make install


License
=======

BSD New, see LICENSE for details.


Links
=====

Documentation:
  http://monad.readthedocs.org/

Issue Tracker:
  https://bitbucket.org/pyx/monad/issues/

Source Package @ PyPI:
  https://pypi.python.org/pypi/monad/

Mercurial Repository @ bitbucket:
  https://bitbucket.org/pyx/monad/

Git Repository @ Github:
  https://github.com/pyx/monad/
