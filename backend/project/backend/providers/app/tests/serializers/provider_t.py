from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse
from backend.accounts.app.models import User
from backend.providers.actions.objects.serializers import ProviderSerializer
from backend.products.actions.objects.serializers import CategorySerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest



class ProviderSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.serializer = ProviderSerializer(instance=cls.providers[1])
        cls.serializer_many = ProviderSerializer(instance=Provider.objects.all(), many=True)
        cls.valid_data = {
            'name': 'test',
            'social_role': 'test',
            'cnpj': '15.684.256/132-96',
            'address': {
                "cep": "15698-789",
                "road": 'road test',
                'complement': 'test',
                'neighborhood': 'test',
            },
            'products': [
                {
                    "product": cls.products[0].name,
                    "price": Decimal(f'{randint(1000, 5000)}.00')
                }
            ],
            'contacts': [
                {
                    'number': '99 99999 9999'
                }
            ]
        }

    def test_default_creation(self):
        test_serializer = ProviderSerializer(data=self.valid_data)
        self.assertTrue(test_serializer.is_valid())

    def test_data_for_serializer(self):
        provider = {
            'id': self.providers[1].id,
            'name': self.providers[1].name,
            'social_role': self.providers[1].social_role,
            'cnpj': self.providers[1].cnpj,
            'address': {
                'id': self.providers[1].address.id,
                "cep": self.providers[1].address.cep,
                "road": self.providers[1].address.road,
                'complement': self.providers[1].address.complement,
                'neighborhood': self.providers[1].address.neighborhood,
                'number': self.providers[1].address.number,
            },
            'products': [{
                    "id": price.id,
                    "product": price.product.name,
                    "price": str(price.price),
            } for price in self.providers[1].products.all()],
            'contacts': [{
                    'id': contact.id,
                    'number': contact.number
            } for contact in self.providers[1].contacts.all()]
        }
        data = self.serializer.data.copy()
        data['address'] = dict(data['address']) # default is OrderedDict
        data['products'] = [dict(product) for product in data['products']] # default is OrderedDict
        data['contacts'] = [dict(contact) for contact in data['contacts']] # default is OrderedDict
        self.assertEqual(data, provider)

    def test_error_required_fields(self):
        serializer = ProviderSerializer(data={})
        self.assertFalse(serializer.is_valid())
        required_fields = ['name', 'cnpj', 'address']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(serializer.errors[field_name][0]))
    
    def test_unique_name_error(self):
        serializer = ProviderSerializer(data={'name': self.providers[0].name})
        self.assertFalse(serializer.is_valid())
        self.assertEqual('provider with this name already exists.', str(serializer.errors['name'][0]))

    def test_cnpj_format_error(self):
        data = self.valid_data.copy()
        data['cnpj'] = '123546789-00'
        serializer = ProviderSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual('Invalid format, use XX.XXX.XXX/XXX-XX', str(serializer.errors['cnpj'][0]))