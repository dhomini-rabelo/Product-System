from rest_framework import generics
from Core.views.data_control.create import DataControlAndCreateApi
from backend.products.actions.objects.serializers import CategorySerializer, PriceMediatorSerializer, ProductSerializer, CreateProductSerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.products.actions.objects.data_control.filter import product_filter
from backend.products.actions.objects.data_control.selector import product_selector


class ProductListAndCreate(DataControlAndCreateApi):
    filter_function = product_filter.filter_queryset
    selector_function = product_selector.select
    serializer_class = ProductSerializer
    post_serializer_class = CreateProductSerializer
    initial_queryset = Product.objects.all()


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CreateProductSerializer
    queryset = Product.objects.all()


class CategoryListAndCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class PriceMediatorCreate(generics.CreateAPIView):
    serializer_class = PriceMediatorSerializer
    queryset = PriceMediator.objects.all()


class PriceMediatorDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PriceMediatorSerializer
    queryset = PriceMediator.objects.all()


