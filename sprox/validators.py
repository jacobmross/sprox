# -*- coding: utf-8 -*-
# sprox.validators.py

"""
validators Module

Copyright (c) 2008 Christopher Perkins
Original Version by Christopher Perkins 2008
Released under MIT license.
"""
__all__ = [
    'NotEmpty',
    'UnicodeString',
    'UniqueValue'
]

from formencode import FancyValidator, Invalid as InvalidError
from formencode.validators import NotEmpty, UnicodeString as FEUnicodeString


class UnicodeString(FEUnicodeString):
    outputEncoding = None


class UniqueValue(FancyValidator):

    def __init__(self, provider, entity, field_name, *args, **kw):
        self.provider = provider
        self.entity = entity
        self.field_name = field_name
        FancyValidator.__init__(self, *args, **kw)

    def _to_python(self, value, state):
        if not self.provider.is_unique(self.entity, self.field_name, value):
            raise InvalidError(
                'That value already exists',
                value, state)
        return value
