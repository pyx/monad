===================================
monad - a functional python package
===================================

.. note::
  **This project is superseded by Hymn(https://github.com/pyx/hymn)**.
  
  Limited by Python's syntax, there is no way to have a clean implementation
  of do notation, the closest thing is a ``do`` decorator on generator
  functions using ``yield`` as ``<-``, which feels like black magic.

  That's why I stopped shoehorning this into Python, and did a complete
  rewrite in Hy (https://github.com/hylang/hy) a few years ago.

  Being a lisp, or as they say, *Homoiconic Python*, Hy has the most flexible
  syntax (or lack thereof :smile:), with it, I finally can write do notations,
  check this out (for added fun, a ``Lazy`` monad is being demonstrated here,
  we can never have such clean way to write thunk in pure python):

  .. code:: clojure

    => (import [hymn.types.lazy [force]])
    => (require [hymn.types.lazy [lazy]])
    => ;; lazy computation implemented as monad
    => ;; macro lazy creates deferred computation
    => (setv a (lazy (print "evaluate a") 42))
    => ;; the computation is deferred, notice the value is shown as '_'
    => a
    Lazy(_)
    => ;; evaluate it
    => (.evaluate a)
    evaluate a
    42
    => ;; now the value is cached
    => a
    Lazy(42)
    => ;; calling evaluate again will not trigger the computation
    => (.evaluate a)
    42
    => (setv b (lazy (print "evaluate b") 21))
    => b
    Lazy(_)
    => ;; force evaluate the computation, same as calling .evaluate on the monad
    => (force b)
    evaluate b
    21
    => ;; force on values other than lazy return the value unchanged
    => (force 42)
    42
    => (require [hymn.macros [do-monad]])
    => ;; do notation with lazy monad
    => (setv c (do-monad [x (lazy (print "get x") 1) y (lazy (print "get y") 2)] (+ x y)))
    => ;; the computation is deferred
    => c
    Lazy(_)
    => ;; do it!
    => (force c)
    get x
    get y
    3
    => ;; again
    => (force c)
    3

  **So, if you are interested in this package, please try
  Hymn(https://github.com/pyx/hymn) instead**.



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
