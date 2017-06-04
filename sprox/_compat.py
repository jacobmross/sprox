# -*- coding: utf-8 -*-
# sprox._compat.py

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

__all__ = [
    'IS_PYTHON2',
    'string_type',
    'unicode_text',
    'byte_string',
    'zip_longest'
]

import platform
import warnings

from nine import IS_PYTHON2, basestring, bytes, str

if platform.system() == 'Windows':  # pragma: no cover
    WIN = True
else:  # pragma: no cover
    WIN = False

string_type = basestring
unicode_text = str
byte_string = bytes


if IS_PYTHON2:  # pragma: no cover
    from itertools import izip_longest as zip_longest
else:
    from itertools import zip_longest

# Migration helpers
try:
    from sprox.sa.validatorselector import SAValidatorSelector as _SAValidatorSelector

    class SAValidatorSelector(_SAValidatorSelector):

        def __init__(self, *args, **kw):
            warnings.warn('This class has moved to the sprox.sa.validatorselector module.')  # pragma: no cover
            _SAValidatorSelector.__init__(self, *args, **kw)  # pragma: no cover
except ImportError:  # pragma: no cover
    pass  # pragma: no cover


try:
    from sprox.sa.widgetselector import SAWidgetSelector as _SAWidgetSelector

    class SAWidgetSelector(_SAWidgetSelector):

        def __init__(self, *args, **kw):
            warnings.warn('This class has moved to the sprox.sa.widgetselector module.')  # pragma: no cover
            _SAWidgetSelector.__init__(self, *args, **kw)  # pragma: no cover
except ImportError:  # pragma: no cover
    pass  # pragma: no cover
