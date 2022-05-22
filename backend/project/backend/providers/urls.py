from django.urls import path
from .views import *

urlpatterns = [
    path('providers', ProviderListAndCreate.as_view()),
    path('providers/<int:pk>', ProviderDetail.as_view()),
]
