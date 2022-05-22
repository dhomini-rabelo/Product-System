from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('products', ProductDataControlAndCreate.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('categories', CategoryListAndCreate.as_view(), name='categories'),
    path('categories/<int:pk>', CategoryDetail.as_view()),
]
