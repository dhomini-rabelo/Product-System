from types import FunctionType
from rest_framework.serializers import ModelSerializer, ValidationError
from django.db.models.query import QuerySet
from django.db.models import Model


class ManyChildSerializers:

    def get_data(self, instance, validated_data: dict):
        # require self.obj_for_get_related_field_data -> dict[FunctionType]
        related_functions, related_fields_data = self.obj_for_get_related_field_data(), {}
        for related_field in related_functions.keys():
            if related_field not in validated_data.keys(): continue
            get_data: FunctionType = related_functions[related_field]
            related_fields_data[related_field] = get_data(instance, validated_data)
            del validated_data[related_field]
        return related_fields_data, validated_data

    def get_or_error(
        self, queryset: QuerySet, pk_kwargs: dict = {}, error_obj = {}
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            raise ValidationError(error_obj)
        return relationship_instance
    
    def get_or_create_instance(
        self, data: dict, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {}, instance_id: int | None = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            return self.create_instance(data, serializer_class, instance_id, related_name)
        return relationship_instance

    def update_instance(
        self, scope_instance: Model, data_for_update: dict,
    ) -> Model: # for o2o and foreign key
        for attribute_name, value in data_for_update.items():
            if value is None: continue
            setattr(scope_instance, attribute_name, value)
        scope_instance.save()
        return scope_instance        

    def create_or_update_instance(
        self, data: dict, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {}, instance_id: int | None = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()
        delete_id = lambda key: key if not key.endswith('_id') else key[:-3] # delete _id

        if relationship_instance is None:
            obj_data = {delete_id(k):v for k,v in data.items()}
            return self.create_instance(obj_data, serializer_class, instance_id, related_name)
        return self.update_instance(relationship_instance, data)

    def create_or_update_many(
        self, data: list[dict], serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {},  instance_id: int | None = None, related_name: str = ''
    ): # m2m or m2o
        for obj in data:
            adapted_kwargs = {k: obj.get(v)  for k, v in pk_kwargs.items()}
            self.create_or_update_instance(obj, serializer_class, queryset, adapted_kwargs, instance_id, related_name)        

    def create_instance(
        self, data: dict, serializer_class: ModelSerializer,
        instance_id: int | None = None, related_name: str = ''
    ) -> Model: # for o2o and foreign key
        if instance_id is not None:
            data[related_name] = instance_id
        serializer = serializer_class(data=data)
        if serializer.is_valid():
            relationship_instance = serializer.save()
            return relationship_instance
        raise ValidationError(serializer.errors)

    def create_many(
        self, data: list[dict], serializer_class: ModelSerializer,
        instance_id: int | None = None, related_name: str = ''
    ): # m2m or m2o
        for obj in data:
            self.create_instance(obj, serializer_class, instance_id, related_name)

    def error_or_update_instance(
        self, data: dict, queryset: QuerySet, pk_kwargs: dict = {}, error_obj = {}
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            raise ValidationError(error_obj)
        return self.update_instance(relationship_instance, data)
    
    def error_or_update_many(
        self, data: list[dict], queryset: QuerySet, pk_kwargs: dict = {}, error_obj = {}
    ) -> Model: # for foreign key
        for obj in data:
            adapted_kwargs = {k: obj.get(v)  for k, v in pk_kwargs.items()}
            self.error_or_update_instance(obj, queryset, adapted_kwargs, error_obj)

    def _validate_ids_for_delete(self, ids_for_delete: list[int], related_name: str):
        if not isinstance(ids_for_delete, list):
            raise ValidationError({f'delete_{related_name}': f'delete_{related_name} must be a list'})
        if not all([isinstance(id_, int) for id_ in ids_for_delete]):
            raise ValidationError({f'delete_{related_name}': f'delete_{related_name} contains invalid id type'})

    def delete_instances(self, instance: Model, related_name: str, ids_for_delete: list[int]):
        self._validate_ids_for_delete(ids_for_delete, related_name)
        objects_for_delete = []
        
        for id_for_delete in ids_for_delete:
            queryset = getattr(instance, related_name)
            obj = queryset.filter(id=id_for_delete).first()
            if obj is None: raise ValidationError({f'delete_{related_name}': f'id "{id_for_delete}" does not exist'})
            objects_for_delete.append(obj)
                
        for obj in objects_for_delete:
            obj.delete()

    def delete_many_instances(self, instance: Model, fields_for_delete: list[str]):
        for field_for_delete in fields_for_delete:
            ids_for_delete: list[int] | None = self.initial_data.get(f'delete_{field_for_delete}')
            if ids_for_delete is not None: self.delete_instances(instance, field_for_delete, ids_for_delete)
                
                