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



class AddressModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    def test_complement_for_null_value(self):
        self.addresses[1].complement = None
        self.addresses[1].save()

    def test_number_for_null_value(self):
        self.addresses[1].number = None
        self.addresses[1].save()

    @expectedFailure
    def test_cep_error_for_null_value(self):
        self.addresses[1].cep = None
        self.addresses[1].save()

    @expectedFailure
    def test_road_error_for_null_value(self):
        self.addresses[1].road = None
        self.addresses[1].save()

    @expectedFailure
    def test_neighborhood_error_for_null_value(self):
        self.addresses[1].neighborhood = None
        self.addresses[1].save()

    def test_one_to_one_relationship_with_Provider_model(self):
        self.assertEqual(self.addresses[1].provider, Provider.objects.get(address__id=self.addresses[1].id))