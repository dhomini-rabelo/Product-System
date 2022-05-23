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



class PriceMediatorModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    @expectedFailure
    def test_provider_error_for_null_value(self):
        self.prices[1].provider = None
        self.prices[1].save()

    @expectedFailure
    def test_product_error_for_null_value(self):
        self.prices[1].product = None
        self.prices[1].save()

    @expectedFailure
    def test_price_error_for_null_value(self):
        self.prices[1].price = None
        self.prices[1].save()

    def test_foreign_key_relationship_with_Product_model(self):
        self.assertEqual(self.prices[1].product, Product.objects.get(id=self.prices[1].product.id))

    def test_foreign_key_relationship_with_Provider_model(self):
        self.assertEqual(self.prices[1].provider, Provider.objects.get(id=self.prices[1].provider.id))
