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



class CategoryModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)

    @expectedFailure
    def test_name_error_for_max_size(self):
        self.categories[1].name = 'x' * 210
        self.categories[1].save()

    @expectedFailure
    def test_name_error_for_null_value(self):
        self.categories[1].name = None
        self.categories[1].save()

    @expectedFailure
    def test_unique_name_error(self):
        self.categories[1].name = self.categories[2].name
        self.categories[1].save()

    def test_many_to_one_relationship_with_Product_model(self):
        self.assertEqual(list(self.categories[1].products.all()), list(Product.objects.filter(category__id=self.categories[1].id)))