from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse
from backend.accounts.app.models import User
from backend.products.actions.objects.serializers import CategorySerializer, PriceMediatorForProductSerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest



class PriceMediatorSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = PriceMediatorForProductSerializer(instance=cls.prices[1])
        cls.serializer_many = PriceMediatorForProductSerializer(instance=PriceMediator.objects.all(), many=True)
        cls.valid_data_1 = {
            'provider': cls.providers[0].name,
            'price': '5000.50'
        }
        cls.valid_data_2 = {
            'provider': cls.providers[1].id,
            'price': '2000.50'
        }

    def test_default_creation(self):
        test_serializer = PriceMediatorForProductSerializer(data=self.valid_data_1)
        test_serializer2 = PriceMediatorForProductSerializer(data=self.valid_data_2)
        self.assertTrue(test_serializer.is_valid())
        self.assertTrue(test_serializer2.is_valid())

    def test_data_for_serializer(self):
        category = {
            'id': self.prices[1].id,
            'provider': self.prices[1].provider.name,
            'price': str(self.prices[1].price),
        }
        self.assertEqual(self.serializer.data, category)

    def test_error_required_name_field(self):
        serializer = PriceMediatorForProductSerializer(data={})
        self.assertFalse(serializer.is_valid())
        required_fields = ['provider', 'price']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(serializer.errors[field_name][0]))