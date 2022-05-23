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
        cls.path = reverse('products:category_list')
        cls.request = cls.client.get(cls.path, **cls.header)
        cls.valid_data = {
            'name': 'test',
        }

    def test_status(self):
        self.assertEqual(self.request.status_code, 200)

    def test_data(self):
        serializer = CategorySerializer(Category.objects.all(), many=True)
        self.assertEqual(
            self.request.data,
            serializer.data
        )

    def test_post_method(self):
        request = self.client.post(self.path, data=self.valid_data, **self.header)
        self.assertEqual(request.status_code, 201)

    def test_error_required_name_field(self):
        request = self.client.post(self.path, data={}, **self.header)
        self.assertEqual('This field is required.', str(request.data['name'][0]))

    def test_unique_name_error(self):
        data = self.valid_data.copy()
        data = {'name': self.categories[2].name}
        request = self.client.post(self.path, data=data, **self.header)
        self.assertEqual(request.status_code, 400)
        self.assertEqual(str(request.data['name'][0]), 'category with this name already exists.')