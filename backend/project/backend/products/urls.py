from django.urls import path
from .views import *


app_name = 'products'

# duplicate to remove route bug from bar
urlpatterns = [
    path('products/', ProductDataControlAndCreate.as_view()),
    path('products', ProductDataControlAndCreate.as_view(), name='product_list'),

    path('products/<int:pk>/', ProductDetail.as_view()),
    path('products/<int:pk>', ProductDetail.as_view(), name='product_detail'),

    path('categories/', CategoryListAndCreate.as_view()),
    path('categories', CategoryListAndCreate.as_view(), name='category_list'),

    path('categories/<int:pk>/', CategoryDetail.as_view()),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category_detail'),
]
