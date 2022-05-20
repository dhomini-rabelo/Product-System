from ast import For
from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL, CASCADE)
from backend.providers.app.models import Provider




class Category(Model):
    name = CharField(max_length=200, unique=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


class Product(Model):
    name = CharField(max_length=200, unique=True)
    description = TextField()
    category = ForeignKey(Category, on_delete=SET_NULL, null=True, related_name='products')
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)


class PriceMediator(Model):
    product = ForeignKey(Product, on_delete=CASCADE, related_name='providers')
    provider = ForeignKey(Provider, on_delete=CASCADE, related_name='products')
    price = DecimalField(decimal_places=2, max_digits=20)
