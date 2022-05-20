from django.urls import path
from .views import *

urlpatterns = [
    path('providers', ProviderListAndCreate.as_view()),
    path('providers/<int:pk>', ProviderDetail.as_view()),
    path('contacts', ContactCreate.as_view()),
    path('contacts/<int:pk>', ContactDetail.as_view()),
    path('addresses', AddressCreate.as_view()),
    path('addresses/<int:pk>', AddressDetail.as_view()),
]
