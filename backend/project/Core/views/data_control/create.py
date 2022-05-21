from django.shortcuts import get_object_or_404
from Core.views.data_control.view import DataControlApi
from rest_framework.response import Response
from rest_framework import status


class DataControlAndCreateApi(DataControlApi):

    def post(self, request):
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

