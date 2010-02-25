"""
mongokitprovider Module

This contains the class which allows sprox to interface with any database.

Copyright &copy 2009 Jorge Vargas
Original Version by Jorge Vargas 2009
Released under MIT license.
"""
from sprox.iprovider import IProvider
from sprox.util import timestamp
import datetime, inspect

from ming.orm import mapper, FieldProperty, RelationProperty, MappedClass
from ming.orm.property import OneToManyJoin, ManyToOneJoin
from ming import schema as S

from widgetselector import MingWidgetSelector
from validatorselector import MingValidatorSelector
from pymongo import ASCENDING, DESCENDING

class MingProvider(IProvider):
    
    default_widget_selector_type = MingWidgetSelector
    default_validator_selector_type = MingValidatorSelector
    
    def get_field(self, entity, name):
        """Get a field with the given field name."""
        return mapper(entity).property_index[name]

    def get_fields(self, entity):
        """Get all of the fields for a given entity."""
        if inspect.isfunction(entity):
            entity = entity()
        return [prop.name for prop in mapper(entity).properties if isinstance(prop, FieldProperty) or isinstance(prop, RelationProperty)]

    def get_entity(self, name):
        """Get an entity with the given name."""
        return MappedClass._registry[name]

    def get_entities(self):
        """Get all entities available for this provider."""
        return MappedClass._registry.iterkeys()

    def get_primary_fields(self, entity):
        """Get the fields in the entity which uniquely identifies a record."""
        return [self.get_primary_field(entity)]

    def get_primary_field(self, entity):
        """Get the single primary field for an entity"""
        return '_id'

    def _get_meta(self, entity, field_name, metaprop):
        """Returns the value of the given sprox meta property for the field."""
        field = self.get_field(entity, field_name)
        return getattr(field, "sprox_meta", {}).get(metaprop, None)
        
    def get_view_field_name(self, entity, possible_names):
        """Get the name of the field which first matches the possible colums

        :Arguments:
          entity
            the entity where the field is located
          possible_names
            a list of names which define what the view field may contain.  This allows the first
            field that has a name in the list of names will be returned as the view field.
        """
        if possible_names is None:
            possible_names = ('_name', 'name', 'description', 'title')
        fields = self.get_fields(entity)
        for field in fields:
            if self._get_meta(entity, field, 'title'):
                return field
        view_field = None
        for column_name in possible_names:
            for actual_name in fields:
                if column_name == actual_name:
                    view_field = actual_name
                    break
            if view_field:
                break;
            for actual_name in fields:
                if column_name in actual_name:
                    view_field = actual_name
                    break
            if view_field:
                break;
        if view_field is None:
            view_field = fields[0]
        return view_field

    def get_dropdown_options(self, entity_or_field, field_name, view_names=None):
        """Get all dropdown options for a given entity field.

        :Arguments:
          entity_or_field
            either the entity where the field is located, or the field itself
          field_name
            if the entity is specified, name of the field in the entity. Otherwise, None
          view_names
            a list of names which define what the view field may contain.  This allows the first
            field that has a name in the list of names will be returned as the view field.

        :Returns:
        A list of tuples with (id, view_value) as items.

        """
        if field_name is not None:
            field = self.get_field(entity_or_field, field_name)
        else:
            field = entity_or_field
            
        if isinstance(field, FieldProperty):
            schemaitem = S.SchemaItem.make(field.field_type)
            if isinstance(schemaitem, S.OneOf):
                return [ (opt,opt) for opt in schemaitem.options ]
            raise NotImplementedError("get_dropdown_options doesn't know how to get the options for field %r of type %r" % (field, schemaitem))
        
        if not isinstance(field, RelationProperty):
            raise NotImplementedError("get_dropdown_options expected a FieldProperty or RelationProperty field, but got %r" % field)
        join = field._infer_join()
        iter = join.rel_cls.query.find()
        view_field = self.get_view_field_name(join.rel_cls, view_names)
        return [ (obj._id, getattr(obj, view_field)) for obj in iter ]

    def get_relations(self, entity):
        """Get all of the field names in an enity which are related to other entities."""
        return [prop.name for prop in mapper(entity).properties if isinstance(prop, RelationProperty)]

    def is_relation(self, entity, field_name):
        """Determine if a field is related to a field in another entity."""
        return isinstance(self.get_field(entity, field_name), RelationProperty)

    def is_nullable(self, entity, field_name):
        """Determine if a field is nullable."""
        fld = self.get_field(entity, field_name)
        if isinstance(fld, RelationProperty):
            # check the required attribute on the corresponding foreign key field
            fld = fld._infer_join().prop
        return not fld.kwargs.get("required", False)

    def get_default_values(self, entity, params):
        return params

    def _cast_value(self, entity, key, value):
        return value
    
    def create(self, entity, params):
        """Create an entry of type entity with the given params."""
        obj = entity()
        fields = self.get_fields(entity)
        for key,value in params.iteritems():
            if key not in fields:
                continue;
            value = self._cast_value(entity, key, value)
            if value is not None:
                setattr(obj,key,value)
        return obj

    def get_obj(self, entity, params):
        return entity.query.find(params).first()
        
    def get(self, entity, params, fields=None, omit_fields=None):
        return self.dictify(self.get_obj(entity, params), fields, omit_fields)

    def update(self, entity, params):
        """Update an entry of type entity which matches the params."""
        obj = entity.query.find({"_id": params["_id"]}).first()
        params.pop('_id')
        if params.has_key('sprox_id'):
            params.pop('sprox_id')
        if params.has_key('_method'):
            params.pop('_method')
        fields = self.get_fields(entity)
        for key, value in params.iteritems():
            if key not in fields:
                continue;
            value = self._cast_value(entity, key, value)
            if value is not None:
                setattr(obj,key,value)
        return obj

    def delete(self, entity, params):
        """Delete an entry of typeentity which matches the params."""
        obj = entity.query.find({"_id": params["_id"]}).first()
        obj.delete()
        return obj
        
    def query(self, entity, limit=None, offset=None, limit_fields=None, order_by=None, desc=False, **kw):
        if offset is None:
            offset = 0
        iter = entity.query.find(skip=offset)
        if limit is not None:
            iter = iter.limit(limit)
        if order_by is not None:
            if desc:
                dir = DESCENDING
            else:
                dir = ASCENDING
            iter.sort(order_by, dir)
        return iter.count(), iter

    def is_binary(self, entity, name):
        field = self.get_field(entity, name)
        return isinstance(field,S.Binary)

    def relation_fields(self, entity, field_name):
        field = self.get_field(entity, field_name)
        if not isinstance(field, RelationProperty):
            raise TypeError("The field %r is not a relation field" % field)
        return [field._infer_join().prop.name]

    def relation_entity(self, entity, field_name):
        """If the field in the entity is a relation field, then returns the
        entity which it relates to.
        
        :Returns:
          Related entity for the field
        """
        field = self.get_field(entity, field_name)
        return field.related

    def get_field_widget_args(self, entity, field_name, field):
        args = {}
        args['provider'] = self
        args['nullable'] = self.is_nullable(entity, field_name)
        return args

    def is_unique(self, entity, field_name, value):
        iter = entity.query.find({ field_name: value })
        return iter.count() == 0
    
    def is_unique_field(self, entity, field_name):
        for idx in getattr(entity.__mongometa__, "unique_indexes", ()):
            if idx == (field_name,):
                return True
        return False
        
    def dictify(self, obj, fields=None, omit_fields=None):
        if obj is None:
            return {}
        r = {}
        for prop in self.get_fields(obj.__class__):
            if fields and prop not in fields:
                continue

            if omit_fields and prop in omit_fields:
                continue

            value = getattr(obj, prop)
            if value is not None:
                if self.is_relation(obj.__class__, prop):
                    klass = self.relation_entity(obj.__class__, prop)
                    pk_name = self.get_primary_field(klass)
                    if isinstance(value, list):
                        #joins
                        value = [getattr(value, pk_name) for value in value]
                    else:
                        #fks
                        value = getattr(value, pk_name)
            r[prop] = value
        return r
