from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL, CASCADE)


class Address(Model):
    city = CharField(max_length=256)
    country = CharField(max_length=256)


class Provider(Model):
    name = CharField(max_length=200, unique=True)
    social_role = TextField()
    cnpj = CharField(max_length=18)
    address = ForeignKey(Address, on_delete=SET_NULL, null=True)


class Contact(Model):
    provider = ForeignKey(Provider, on_delete=CASCADE, related_name='contacts')
    number = CharField(max_length=30)