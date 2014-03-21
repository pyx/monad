# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.types.null - The Null type."""


class Null(object):
    """Null represents nothing."""
    # pylint: disable = too-few-public-methods
    def __repr__(self):
        return 'Null'

    def __call__(self):
        return self


# pylint: disable = invalid-name
#: The Null object.
Null = Null()
