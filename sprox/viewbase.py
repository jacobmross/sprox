import inspect
from tw.api import Widget
from tw.forms import HiddenField
from configbase import ConfigBase, ConfigBaseError
from sqlalchemy.orm import PropertyLoader
from sqlalchemy.schema import Column
from widgetselector import WidgetSelector

#sa 0.5 support
try:  #pragma:no cover
    from sqlalchemy.types import Enum
except:  #pragma:no cover
    class Enum:
        pass

class ClassViewer(object):
    """class wrapper to expose items of a class.  Needed to pass classes to TW as params"""
    def __init__(self, klass):
        self.__name__ = klass.__name__


class ViewBaseError(Exception):pass

class ViewBase(ConfigBase):
    """

    :Modifiers:

    +-----------------------------------+--------------------------------------------+------------------------------+
    | Name                              | Description                                | Default                      |
    +===================================+============================================+==============================+
    | __widget_selector_type__          | What class to use for widget selection.    | WidgetSelector               |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_widgets__                 | A dictionary of widgets to replace the     | {}                           |
    |                                   | ones that would be chosen by the selector  |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_widget_types__            | A dictionary of types of widgets, allowing | {}                           |
    |                                   | sprox to determine the widget args         |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __field_widget_args__             | A dictionary of types of args for widgets, | {}                           |
    |                                   | you to override the args sent to the fields|                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __base_widget_type__              | The base widget for this config            | Widget                       |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __base_widget_args__              | Args to pass into the widget overrides any | {}                           |
    |                                   | defaults that are set in sprox creation    |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+
    | __widget_selector__               | an instantiated object to use for widget   | None                         |
    |                                   | selection.                                 |                              |
    +-----------------------------------+--------------------------------------------+------------------------------+

    Also, see the :mod:`sprox.configbase` modifiers.
    """
    __field_widgets__      = None
    __field_widget_types__ = None
    __field_widget_args__  = None
    __ignore_field_names__ = None

    #object overrides
    __base_widget_type__       = Widget
    __base_widget_args__       = None
    __widget_selector_type__   = WidgetSelector
    __widget_selector__        = None


    def _do_init_attrs(self):
        super(ViewBase, self)._do_init_attrs()
        if self.__base_widget_args__ is None:
            self.__base_widget_args__ = {}
        if self.__field_widgets__ is None:
            self.__field_widgets__ = {}
        if self.__field_widget_args__ is None:
            self.__field_widget_args__ = {}
        if self.__field_widget_types__ is None:
            self.__field_widget_types__ = {}
        if self.__widget_selector__ is None:
            self.__widget_selector__ = self.__widget_selector_type__()

        if self.__ignore_field_names__ is None:
            self.__ignore_field_names__ = ['sprox_id', '_method']

        for attr in dir(self):
            if not attr.startswith('__'):
                value = getattr(self, attr)
                if isinstance(value, Widget):
                    if not getattr(value, 'id', None):
                        raise ViewBaseError('Widgets must provide an id argument for use as a field within a ViewBase')
                    self.__add_fields__[attr] = value
                try:
                    if issubclass(value, Widget):
                        self.__field_widget_types__[attr] = value
                except TypeError:
                    pass

    @property
    def __widget__(self):
        widget = getattr(self, '___widget__', None)
        if not widget:
            self.___widget__ = self.__base_widget_type__(**self.__widget_args__)
            widget = self.___widget__
        return self.___widget__

    #try to act like a widget as much as possible
    def __call__(self, *args, **kw):
        return self.__widget__.__call__(*args, **kw)

    @property
    def __widget_args__(self):
        return self._do_get_widget_args()

    def _do_get_widget_args(self):
        widget_dict = self._do_get_field_widgets(self.__fields__)

        field_widgets = []
        for key in self.__fields__:
            if key not in widget_dict:
                continue
            value = widget_dict[key]
            #sometimes a field will have two widgets associated with it (disabled fields)
            if hasattr(value,'__iter__'):
                field_widgets.extend(value)
                continue
            field_widgets.append(value)

        d = dict(children=field_widgets)
        d.update(self.__base_widget_args__)
        return d

    def _do_get_disabled_fields(self):
        return self.__disable_fields__

    def _do_get_field_widget_args(self, field_name, field):
        # toscawidgets does not like ids that have '.' in them.  This does not
        # work for databases with schemas.
        field_name = field_name.replace('.', '_')
        args = {}

        #this is sort of a hack around TW evaluating _some_ params that are classes.
        entity = field
        if inspect.isclass(field):
            entity = ClassViewer(field)

        args = {'id':field_name, 'identity':self.__entity__.__name__+'_'+field_name, 'entity':entity}
        if isinstance(entity, Column) and entity.default:
            if isinstance(entity.default.arg, str) or \
               isinstance(entity.default.arg, unicode) or \
               isinstance(entity.default.arg, int) or \
               isinstance(entity.default.arg, float):
                    args['default'] = entity.default.arg

        #enum support works completely differently.
        #if isinstance(entity, Column) and isinstance(entity.type, Enum):
        #    args['options'] = entity.type.enums

        if field_name in self.__field_attrs__:
            args['attrs'] = self.__field_attrs__[field_name]

        if isinstance(field, PropertyLoader):
            args['provider'] = self.__provider__
            args['nullable'] = self.__provider__.is_nullable(self.__entity__, field_name)

        if field_name in self.__field_widget_args__:
            args.update(self.__field_widget_args__[field_name])
        return args

    def __create_hidden_fields(self):
        fields = {}
        fields['sprox_id'] = HiddenField(id='sprox_id')

        for field in self.__hide_fields__:
            if field not in self.__omit_fields__:
                args = {}
                if field in self.__field_widget_args__:
                    args.update(self.__field_widget_args__[field])
                fields[field] = HiddenField(id=field, identifier=field, **args)

        return fields

    def _do_get_field_widgets(self, fields):

        metadata_keys = self.__metadata__.keys()
        widgets = {}
        for field_name in fields:
            if field_name in self.__field_widgets__:
                widgets[field_name] = self.__field_widgets__[field_name]
                continue
            if field_name in self.__add_fields__:
                widget = self.__add_fields__[field_name]
                if widget is None:
                    widget = Widget(field_name)
                widgets[field_name] = widget
                continue
            if field_name in self.__ignore_field_names__:
                continue
            if field_name in self.__hide_fields__:
                continue
            if field_name not in metadata_keys:
                continue
            field = self.__metadata__[field_name]

            if inspect.isclass(field):
                identifier = ClassViewer(field)

            field_widget_type = self.__field_widget_types__.get(field_name,
                                                                self.__widget_selector__.select(field))
            field_widget_args = self._do_get_field_widget_args(field_name, field)

            if field_name in self._do_get_disabled_fields():
                # in this case, we display the current field, disabling it, and also add
                # a hidden field into th emix
                field_widget_args['disabled'] = True
                widgets[field_name] = (HiddenField(id=field_name.replace('.','_'), identifier=field_name), field_widget_type(**field_widget_args))
            else:
                widgets[field_name] = field_widget_type(**field_widget_args)

        widgets.update(self.__create_hidden_fields())
        return widgets
