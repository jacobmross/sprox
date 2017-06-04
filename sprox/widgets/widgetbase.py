# -*- coding: utf-8 -*-
# sprox.widgets.widgetbase.py

from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals
)

__all__ = [
    'HAS_TW2',

    # tw direct imports
    'Widget',
    'HiddenField',
    'TableForm',
    'Column',
    'WidgetMeta',  # tw2 only
    'Deferred',  # tw2 only

    # sprox.widgets.tw#widgets imports
    'ContainerWidget',
    'EntityDefWidget',
    'EntityLabelWidget',
    'ModelLabelWidget',
    'PropertyMultipleSelectField',
    'PropertySingleSelectField',
    'RecordFieldWidget',
    'RecordViewWidget',
    'SproxCalendarDatePicker',
    'SproxCalendarDateTimePicker',
    'SproxCheckBox',
    'SproxDataGrid',
    'SproxMethodPutHiddenField',
    'SproxTimePicker',
    'SubDocument',
    'TableDefWidget',
    'TableLabelWidget',
    'TableWidget',
    'CalendarBase',  # tw2 only
    'Label',  # tw2 only
    'SubDocumentsList',  # tw2 only
    'PropertyMixin',  # tw1 only
    'SproxTableForm',  # tw1 only
]

try:  # pragma: no cover
    import tw2.core as twc
    import tw2.forms as twf
    import sprox.tw2widgets.widgets as _sprox_widgets
    HAS_TW2 = True
except ImportError:  # pragma: no cover
    HAS_TW2 = False
    import tw.api as twc
    import tw.forms as twf
    import sprox.tw1widgets.widgets as _sprox_widgets
finally:  # pragma: no cover
    from twc import Widget
    from twf import HiddenField, TableForm
    from twf.datagrid import Column
    from _sprox_widgets import (
        ContainerWidget,
        EntityDefWidget,
        EntityLabelWidget,
        ModelLabelWidget,
        PropertyMultipleSelectField,
        PropertySingleSelectField,
        RecordFieldWidget,
        RecordViewWidget,
        SproxCalendarDatePicker,
        SproxCalendarDateTimePicker,
        SproxCheckBox,
        SproxDataGrid,
        SproxMethodPutHiddenField,
        SproxTimePicker,
        SubDocument,
        TableDefWidget,
        TableLabelWidget,
        TableWidget
    )


if HAS_TW2:
    from twc import Deferred
    from twc.widgets import WidgetMeta
    from twf import CalendarBase
    from _sprox_widgets import Label, SubDocumentsList

    class PropertyMixin(object):
        pass

    class SproxTableForm(object):
        pass

else:  # presume tw1
    from _sprox_widgets import PropertyMixin, SproxTableForm

    class Deferred(object):
        """TW2 DeferredClass"""
        pass

    class WidgetMeta(object):
        """TW2 WidgetMetaClass"""
        pass

    class CalendarBase(object):
        pass

    class Label(object):
        pass

    class SubDocumentsList(object):
        pass
