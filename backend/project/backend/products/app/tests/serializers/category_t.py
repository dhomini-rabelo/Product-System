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



class CategorySerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = CategorySerializer(instance=cls.categories[1])
        cls.serializer_many = CategorySerializer(instance=Category.objects.all(), many=True)
        cls.valid_data = {
            'name': 'test',
        }

    def test_default_creation(self):
        test_serializer = CategorySerializer(data=self.valid_data)
        self.assertTrue(test_serializer.is_valid())

    def test_data_for_serializer(self):
        category = {
            'id': self.categories[1].id,
            'name': self.categories[1].name           
        }
        self.assertEqual(self.serializer.data, category)

    def test_error_required_name_field(self):
        serializer = CategorySerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEqual('This field is required.', str(serializer.errors['name'][0]))
    
    def test_unique_name_error(self):
        serializer = CategorySerializer(data={'name': self.categories[0].name})
        self.assertFalse(serializer.is_valid())
        self.assertEqual('category with this name already exists.', str(serializer.errors['name'][0]))