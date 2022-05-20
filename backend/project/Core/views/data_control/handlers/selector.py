from dataclasses import field
from typing import Any, Type
from django.db.models.query import QuerySet
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from Core.views.data_control.exceptions import ModelNotFound
from backend.products.actions.objects import serializers


class SelectorForQueryset:
    """
    The class manages fields from some ModelSerializer | ListSerializer
    """
    selector_name_in_body = 'selector'
    selector_model_name_in_body = 'selector_model'
    simple_fields_name_in_body = 'fields'
    relationship_fields_name_in_body = 'relationship_fields'

    def __init__(self, models = {}, is_many: bool = True):
        self.models = models # request.body models
        self.is_many = is_many

    def select(self, queryset: QuerySet, SerializerClass: ModelSerializer | ListSerializer, body: dict) -> ReturnDict | ReturnList:
        """
        Select fields from some serializer for serialization

        Args:
            queryset (QuerySet): Initial queryset
            SerializerClass (ModelSerializer| ListSerializer): Default serializer class
            body (dict): matches a request.body

        Local Variables:
            selector ( dict | None ): Obj for manages selected fields
            simple_fields ( list[str] | None ): Selected fields from initial serializer class
            relationship_fields ( dict[str, list] | None ): Selected fields from relationship fields

        Returns:
            ReturnDict | ReturnList: Serialized queryset
        """
        selector: dict | None = self._get_selector(body)
        if selector is None: return self._get_response(SerializerClass, queryset)

        simple_fields: list[str] | None = selector.get(self.simple_fields_name_in_body)
        relationship_fields: dict[str, list] | None = selector.get(self.relationship_fields_name_in_body)
        if simple_fields is not None:
            SerializerCopy = self._get_serializer_copy_class(SerializerClass, simple_fields, relationship_fields, False)     
            return self._get_response(SerializerCopy, queryset)

        return self._get_response(SerializerClass, queryset)

    def _get_selector(self, body: dict) -> None | dict:
        model = body.get(self.selector_model_name_in_body)
        custom_selector = body.get(self.selector_name_in_body)
        if model in self.models.keys():
            return self.models[model]
        elif model is not None:
            raise ModelNotFound(f'{model} not found in {list(self.models.keys())}') # invalid model name
        elif custom_selector is not None:
            self._validate_selector(custom_selector)
        return custom_selector     

    def _validate_selector(self, selector: Any):
        self._validate_type_and_length(self.selector_name_in_body, selector, dict)

    def _validate_args_for__get_serializer_copy_class(self, serializer_fields: Any, relationship_fields: Any):
        self._validate_type_and_length(self.simple_fields_name_in_body, serializer_fields, list)
        if relationship_fields is not None:
            self._validate_type_and_length(self.relationship_fields_name_in_body, relationship_fields, dict)
            if not all([ isinstance(relationship_fields[key], list) and len(relationship_fields[key]) > 0 for key in relationship_fields.keys()]):
                raise ValueError('Invalid relationship_field value, value must be a list with length > 0')

    def _validate_type_and_length(self, name: str, obj: Any, types: Type | tuple[Type]):
        if not isinstance(obj, types): raise TypeError(f'"{name}" must be a {types}')
        if len(obj) == 0: raise ValueError(f'"{name}" is empty')

    def _get_serializer_copy_class(
            self, SerializerClass: ModelSerializer, serializer_fields: list, 
            relationship_fields: None | dict[str, list] = None, is_instance: bool = True
        ) -> ModelSerializer | ListSerializer:
        self._validate_args_for__get_serializer_copy_class(serializer_fields, relationship_fields)

        if relationship_fields is None:
            if not is_instance:
                serializer_class, Dad = SerializerClass, SerializerClass
            elif isinstance(SerializerClass, ListSerializer):
                serializer_class, Dad = SerializerClass.child, SerializerClass.child.__class__
            else: 
                serializer_class, Dad = SerializerClass.__class__, SerializerClass.__class__
            

            class SerializerCopy(Dad):

                class Meta:
                    model = serializer_class.Meta.model
                    fields = serializer_fields

        elif not all([field in serializer_fields for field in list(relationship_fields.keys())]):
            # prevents extra processing
            raise ValueError(f'Some relationship field not in {self.simple_fields_name_in_body}')
            
        else:
            fields = SerializerClass().get_fields()
            relationship_fields_serializers = {
                field: self._get_serializer_copy_class(fields[field], field_list) for field, field_list in relationship_fields.items() 
            }

            class SerializerCopy(SerializerClass):
                for field, serializer in relationship_fields_serializers.items():
                    is_many = isinstance(fields[field], ListSerializer)
                    vars()[field] = serializer(many=is_many)
                
                class Meta:
                    model = SerializerClass.Meta.model
                    fields = serializer_fields
            
        return SerializerCopy

    def _get_response(self, SerializerClass: ModelSerializer, queryset: QuerySet) -> ReturnDict | ReturnList:
        serializer = SerializerClass(queryset, many=self.is_many)
        return serializer.data