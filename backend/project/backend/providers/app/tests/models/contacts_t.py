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
from backend.providers.app.models import Address, Contact, Provider
from test.backend.base import BaseClassForTest



class ContactModelTest(BaseClassForTest):

    @classmethod
    def setUpTestData(cls):
        cls.create_models(cls)
        cls.contact = cls.providers[1].contacts.first()

    @expectedFailure
    def test_number_error_for_null_value(self):
        self.contact.number = None
        self.contact.save()

    def test_many_to_one_relationship_with_Product_model(self):
        self.assertEqual(list(self.providers[1].contacts.all()), list(Contact.objects.filter(provider__id=self.providers[1].id)))