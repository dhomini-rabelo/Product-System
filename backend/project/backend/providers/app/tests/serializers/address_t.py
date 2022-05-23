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
from backend.providers.actions.objects.serializers import AddressSerializer
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest



class AddressSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = AddressSerializer(instance=cls.addresses[1])
        cls.serializer_many = AddressSerializer(instance=Address.objects.all(), many=True)
        cls.valid_data = {
            "cep": "15698-789",
            "road": 'road test',
            'complement': 'test',
            'neighborhood': 'test',
        }

    def test_default_creation(self):
        test_serializer = AddressSerializer(data=self.valid_data)
        self.assertTrue(test_serializer.is_valid())

    def test_data_for_serializer(self):
        address = {
            "id": self.addresses[1].id,
            "cep": self.addresses[1].cep,
            "road": self.addresses[1].road,
            'complement': self.addresses[1].complement,
            'neighborhood': self.addresses[1].neighborhood,
            'number': self.addresses[1].number,
        }
        self.assertEqual(self.serializer.data, address)

    def test_error_required_fields(self):
        serializer = AddressSerializer(data={})
        self.assertFalse(serializer.is_valid())
        required_fields = ['cep', 'road', 'neighborhood']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(serializer.errors[field_name][0]))
    