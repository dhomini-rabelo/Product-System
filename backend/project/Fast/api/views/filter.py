from Fast.django.api.main import apply_filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status



class FilterView(APIView):

    def get(self, request):
        filter_process = apply_filters(self.model, self.filter_obj, request.GET)
        if filter_process.get('error'):
            return Response(filter_process, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(filter_process['model'], many=True)
        return Response(serializer.data)
        