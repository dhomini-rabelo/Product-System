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



class CategoryListAndCreateTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.client = Client()
        cls.header = cls.get_header(cls)
        cls.pk = cls.categories[0].id
        cls.path = reverse('products:category_detail', kwargs={'pk': cls.pk})
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': 'test',
        }

    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = CategorySerializer(Category.objects.get(id=self.pk))
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_put_method(self):
        data = self.valid_data.copy()
        request = self.client.put(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_patch_method(self):
        data = {'name': 'patch'}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 200)
        self.assertEqual(request.data['name'], data['name'])

    def test_delete_method(self):
        path = reverse('products:category_detail', kwargs={'pk': self.categories[1].id})
        request = self.client.delete(path, **self.header)
        self.assertEqual(request.status_code, 204) # 204 - NO CONTENT

    def test_put_error_required_name_field(self):
        request = self.client.put(self.path, data={}, **self.header)
        self.assertEqual('This field is required.', str(request.data['name'][0]))

    def test_unique_name_error(self):
        data = {'name': self.categories[2].name}
        request = self.client.patch(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['name'][0]), 'category with this name already exists.')