from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL, CASCADE, OneToOneField)



class Address(Model):
    cep = CharField(max_length=9) # XXXXX-XXX
    road = CharField(max_length=200)
    complement = CharField(max_length=200)
    neighborhood = CharField(max_length=200)
    number = CharField(max_length=20, blank=True, null=True)


class Provider(Model):
    name = CharField(max_length=200, unique=True)
    social_role = TextField(blank=True, null=True)
    cnpj = CharField(max_length=17, unique=True) # XX.XXX.XXX/XXX-XX
    address = OneToOneField(Address, on_delete=SET_NULL, null=True)


class Contact(Model):
    provider = ForeignKey(Provider, on_delete=CASCADE, related_name='contacts')
    number = CharField(max_length=50) # to accept more number formats