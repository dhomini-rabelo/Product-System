from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse
from backend.accounts.app.models import User
from backend.products.actions.objects.serializers import CategorySerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest



class ProviderModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    def test_social_role_for_null_value(self):
        self.providers[1].social_role = None
        self.providers[1].save()

    @expectedFailure
    def test_name_error_for_null_value(self):
        self.providers[1].name = None
        self.providers[1].save()

    @expectedFailure
    def test_unique_name_error(self):
        self.providers[1].name = self.providers[2].name
        self.providers[1].save()

    @expectedFailure
    def test_unique_cnpj_error(self):
        self.providers[1].cnpj = self.providers[2].cnpj
        self.providers[1].save()

    def test_one_to_one_relationship_with_Address_model(self):
        self.assertEqual(self.providers[1].address, Address.objects.get(id=self.providers[1].address.id))

    def test_many_to_one_relationship_with_Price_Mediator_model(self):
        self.assertEqual(list(self.providers[1].products.all()), list(PriceMediator.objects.filter(provider__id=self.providers[1].id)))