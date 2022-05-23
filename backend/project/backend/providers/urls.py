from django.urls import path
from .views import *


app_name = 'providers'


urlpatterns = [
    path('providers', ProviderDataControlAndCreate.as_view(), name='provider_list'),
    path('providers/<int:pk>', ProviderDetail.as_view(), name='provider_detail'),
]
