from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models.query import QuerySet
from collections.abc import Iterable
from Fast.utils.main import get_type_name
from abc import ABC # abstract class
from rest_framework.serializers import ModelSerializer, ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class DataControlApi(APIView, ABC):
    """
    This class apply filters and serializer a queryset based in request.body

    Require variables:
        serializer_class ( ModelSerializer ) : The default serializer class
        initial_queryset ( Queryset ) : The default queryset
        filter_function ( Function(self, queryset: QuerySet, body: dict) -> QuerySet ) : This function filter initial_queryset based in request.body
        selector_function ( Function(self, queryset: QuerySet, serializer: ModelSerializer, body: dict) -> ModelSerializer.data | ListSerializer.data ) : This function
        select fields and returns response based in request.body
    """

    def get(self, request) -> ReturnDict | ReturnList:
        try:
            body = self._get_body(request)
            initial_queryset = self.get_queryset()
            new_queryset = self.filter_function(initial_queryset, body)
            response = self.selector_function(new_queryset, self.get_serializer_class(), body)
        except Exception as error:
            return Response({get_type_name(error): str(error)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(response)

    def _get_body(self, request):
        body = request.data or {}
        if not isinstance(body, dict): raise TypeError('Body must be a dict')
        return body

    def get_queryset(self) -> QuerySet:
        return self.initial_queryset

    def get_serializer_class(self) -> ModelSerializer | ListSerializer:
        return self.serializer_class