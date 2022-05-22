from django.urls import path
from .views import *

urlpatterns = [
    path('providers', ProviderDataControlAndCreate.as_view()),
    path('providers/<int:pk>', ProviderDetail.as_view()),
]
