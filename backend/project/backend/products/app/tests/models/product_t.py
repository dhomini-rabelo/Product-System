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



class ProductModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    def test_description_for_null_value(self):
        self.products[1].description = None
        self.products[1].save()

    @expectedFailure
    def test_name_error_for_max_size(self):
        self.products[1].name = 'x' * 210
        self.products[1].save()

    @expectedFailure
    def test_name_error_for_null_value(self):
        self.products[1].name = None
        self.products[1].save()

    @expectedFailure
    def test_unique_name_error(self):
        self.products[1].name = self.products[2].name
        self.products[1].save()

    def test_one_to_many_relationship_with_Product_model(self):
        self.assertEqual(self.products[1].category, Category.objects.get(id=self.products[1].category.id))

    def test_many_to_one_relationship_with_Price_Mediator_model(self):
        self.assertEqual(list(self.products[1].providers.all()), list(PriceMediator.objects.filter(product__id=self.products[1].id)))