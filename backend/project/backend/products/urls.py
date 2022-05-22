from django.urls import path
from .views import *

urlpatterns = [
    path('products', ProductDataControlAndCreate.as_view()),
    path('products/<int:pk>', ProductDetail.as_view()),
    path('categories', CategoryListAndCreate.as_view()),
    path('categories/<int:pk>', CategoryDetail.as_view()),
]
