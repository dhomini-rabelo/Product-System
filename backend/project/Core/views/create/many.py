from rest_framework.serializers import ModelSerializer, ValidationError
from django.db.models.query import QuerySet
from django.db.models import Model


class CreatorForSerializerWithManyFields:

    def get_or_create_instance(
        self, data: dict, serializer_class: ModelSerializer, queryset: QuerySet,
        pk_kwargs: dict = {}, instance_id: int | None = None, related_name: str = '',
    ) -> Model: # for foreign key
        relationship_instance = queryset.filter(**pk_kwargs).first()

        if relationship_instance is None:
            return self.create_instance(data, serializer_class, instance_id, related_name)
        return relationship_instance

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