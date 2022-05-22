from django.test import TestCase, Client
from unittest import expectedFailure
from random import randint
from django.db.models import Model
from decimal import Decimal
from datetime import date
from backend.accounts.app.models import User
from backend.products.app.models import Category, PriceMediator, Product
from backend.providers.app.models import Address, Provider



class BaseClassForTest(TestCase):

    def create_models(self):
        self.categories = [Category(name=name) for name in ['tecnologia', 'esporte', 'casa', 'carro', 'ferramentas']]
        Category.objects.bulk_create(self.categories)

        self.providers, self.addresses, self.products = [], [], []
        data_range = range(1, 11)
        for i in data_range:
            n = lambda : randint(1, 99999999999999999999)

            self.products.append(Product(
                name=f'product {n()}',
                description=f'product description {i}',
                category=self.categories[randint(0, len(self.categories) - 1)]
            ))

            provider = Provider(
                name=f'provider {n()}',
                social_role=f'provider social_role {i}',
                cnpj=f'{randint(10, 99)}.{randint(100, 999)}.{randint(100, 999)}/{randint(100, 999)}-{randint(10, 99)}'
            )

            address = Address(
                cep=f'{randint(10000, 99999)}-{randint(100, 999)}',
                road=f'road {i}',
                complement=f'complement {i}',
                neighborhood=f'neighborhood {i}',
                number=f'{randint(1, 99999)}'
            )

            provider.address = address
            self.addresses.append(address)
            self.providers.append(provider)

        Address.objects.bulk_create(self.addresses)
        Provider.objects.bulk_create(self.providers)
        Product.objects.bulk_create(self.products)

        self.prices = []
        for i in data_range:
            self.prices.append(PriceMediator(
                product_id=i,
                provider_id=i,
                price=Decimal(f'{randint(100, 100000)}.00')
            ))
        PriceMediator.objects.bulk_create(self.prices)

    def get_header(self):
        return {'content_type': 'application/json'}

        