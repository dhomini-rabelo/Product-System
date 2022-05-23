from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from django.urls import reverse, resolve
from backend.accounts.app.models import User
from backend.products.actions.objects.serializers import CategorySerializer, ProductSerializer
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.actions.objects.serializers import ProviderSerializer
from backend.providers.app.models import Address, Provider
from test.backend.base import BaseClassForTest
from django.db.models import Q



class ProviderDataControlAndCreateTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.header = cls.get_header(cls)
        cls.path = reverse('providers:provider_list')
        cls.request = cls.client.get(cls.path, **cls.header)
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

    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = ProviderSerializer(Provider.objects.all(), many=True)
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_post_method(self):
        request = self.client.post(self.path, data=self.valid_data, **self.header)
        self.assertEqual(request.status_code, 201)

    def test_product_not_found_error(self):
        data = self.valid_data.copy()
        data['products'] = [{'price': Decimal('1000.50'), 'product': 'invalid_product_name'}]
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['products'][0][0]), 'Product not found')

    def test_required_field_error(self):
        request = self.client.post(self.path, data={}, **self.header)
        required_fields = ['name', 'cnpj', 'address']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(request.data[field_name][0]))

    def test_cnpj_format_error(self):
        data = self.valid_data.copy()
        data['cnpj'] = '123456789-99'
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['cnpj'][0]), 'Invalid format, use XX.XXX.XXX/XXX-XX')

    def test_cep_format_error(self):
        data = self.valid_data.copy()
        data['address'] = {**data['address'], 'cep': '123456'}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['address']['cep'][0]), 'Invalid format, use XXXXX-XXX')

    def test_unique_name_error(self):
        data = self.valid_data.copy()
        data = {'name': self.providers[1].name}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['name'][0]), 'provider with this name already exists.')

    def test_unique_cnpj_error(self):
        data = self.valid_data.copy()
        data = {'cnpj': self.providers[1].cnpj}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['cnpj'][0]), 'provider with this cnpj already exists.')
