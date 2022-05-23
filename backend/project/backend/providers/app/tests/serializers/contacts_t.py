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
from backend.providers.actions.objects.serializers import ContactSerializer
from backend.providers.app.models import Address, Contact, Provider
from test.backend.base import BaseClassForTest



class ContactSerializerTest(BaseClassForTest):
    
    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.contact = Contact.objects.create(number='91 11111 1111', provider_id=1)
        cls.serializer = ContactSerializer(instance=cls.contact)
        cls.serializer_many = ContactSerializer(instance=Contact.objects.all(), many=True)
        cls.valid_data = {
            'number': '98 99999 9999',
            'provider': 7 # id
        }

    def test_default_creation(self):
        test_serializer = ContactSerializer(data=self.valid_data)
        self.assertTrue(test_serializer.is_valid())

    def test_data_for_serializer(self):
        contact = {
            'id': self.contact.id,
            'number': self.contact.number           
        }
        self.assertEqual(self.serializer.data, contact)

    def test_error_required_name_field(self):
        serializer = ContactSerializer(data={})
        self.assertFalse(serializer.is_valid())
        required_fields = ['number']
        for field_name in required_fields:
            self.assertEqual('This field is required.', str(serializer.errors[field_name][0]))
    