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
        categories = [Category(name=name) for name in ['tecnologia', 'esporte', 'casa']]
        Category.objects.bulk_create(categories)

        providers, addresses, products = [], [], []
        for i in range(1, 11):
            n = lambda : randint(1, 99999999999999999999)

            products.append(Product(
                name=f'product {n()}',
                description=f'product description {i}',
                category=categories[randint(0, len(categories) - 1)]
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
            addresses.append(address)
            providers.append(provider)

        Address.objects.bulk_create(addresses)
        Provider.objects.bulk_create(providers)
        Product.objects.bulk_create(products)

        for i in range(1, 11):
            PriceMediator.objects.create(
                product_id=i,
                provider_id=i,
                price=Decimal(f'{randint(100, 100000)}.00')
            )

    def get_header(self):
        return {'content_type': 'application/json'}

        