# -*- coding: utf-8 -*-
# Copyright (c) 2012-2014, Philip Xu <pyx@xrefactor.com>
# License: BSD New, see LICENSE for details.
"""monad.exceptions - custom exceptions."""


class ExtractError(Exception):
    """Raised when failed to extract value from monad."""
    def __init__(self, monad):
        super(ExtractError, self).__init__(
            'cannot extract value from {}'.format(repr(monad)))
        self.monad = monad
