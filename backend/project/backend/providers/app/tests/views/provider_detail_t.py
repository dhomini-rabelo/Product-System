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



class ProviderDetail(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.header = cls.get_header(cls)
        provider = cls.providers[0]
        cls.pk = provider.id
        cls.path = reverse('providers:provider_detail', kwargs={'pk': cls.pk})
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': provider.name,
            'social_role': provider.name,
            'cnpj': provider.cnpj,
            'address': {
                "cep": provider.address.cep,
                "road": provider.address.road,
                'complement': provider.address.complement,
                'neighborhood': provider.address.neighborhood,
            },
            'products': [
            ],
            'contacts': [
            ]
        }
    
    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = ProviderSerializer(Provider.objects.get(id=self.pk))
        self.assertEqual(
            self.request.data,
            serializer.data
        )
    
    def test_put_method(self):
        data = self.valid_data.copy()
        data['name'] = 'new name'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_patch_method(self):
        data = {'name': 'patch name'}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_delete_method(self):
        path = reverse('providers:provider_detail', kwargs={'pk': self.providers[3].id})
        request = self.client.delete(path, **self.header)
        self.assertEqual(request.status_code, 204)

    def test_create_and_change_product_instance(self):
        product_name = self.products[1].name # id != 0
        product_data = {'product': product_name, 'price': '50.00'}
        data = {'products': [product_data]}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertIn(product_data, [{'product': product['product'], 'price': product['price']} for product in request.data['products']])
        # test change
        new_product_data = {'product': product_name, 'price': '100.00'}
        data = {'products': [new_product_data]}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertIn(new_product_data, [{'product': product['product'], 'price': product['price']} for product in request.data['products']])

    def test_required_field_error(self):
        request = self.client.put(self.path, data={}, **self.header)
        required_fields = ['name', 'cnpj', 'address']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(request.data[field_name][0]))

    def test_provider_not_found_error(self):
        request = self.client.patch(self.path, data={'products': [{'product': 'not_found_name', 'price': '50.00'}]}, **self.header)
        self.assertEqual(str(request.data['products'][0][0]), 'Product not found')

    def test_cnpj_format_error(self):
        data = self.valid_data.copy()
        data['cnpj'] = '123456789-99'
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['cnpj'][0]), 'Invalid format, use XX.XXX.XXX/XXX-XX')

    def test_cep_format_error(self):
        data = self.valid_data.copy()
        data['address'] = {**data['address'], 'cep': '123456'}
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['address']['cep'][0]), 'Invalid format, use XXXXX-XXX')