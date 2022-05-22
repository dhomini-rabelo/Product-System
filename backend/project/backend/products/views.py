from rest_framework import generics
from Core.support.renders import SimpleRenderer
from Core.views.data_control.create import DataControlAndCreateApi
from backend.products.actions.objects.serializers import CategorySerializer, ProductSerializer
from backend.products.app.models import Category, Product
from backend.products.actions.objects.data_control.filter import product_filter
from backend.products.actions.objects.data_control.selector import product_selector


class ProductListAndCreate(SimpleRenderer, DataControlAndCreateApi): # order is important
    filter_function = product_filter.filter_queryset
    selector_function = product_selector.select
    serializer_class = ProductSerializer
    initial_queryset = Product.objects.all().select_related('category').prefetch_related('providers')


class ProductDetail(SimpleRenderer, generics.RetrieveUpdateDestroyAPIView): # order is important
    serializer_class = ProductSerializer
    queryset = Product.objects.all().select_related('category').prefetch_related('providers')


class CategoryListAndCreate(SimpleRenderer, generics.ListCreateAPIView): # order is important
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(SimpleRenderer, generics.RetrieveUpdateDestroyAPIView): # order is important
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


