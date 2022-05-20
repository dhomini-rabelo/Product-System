from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe
from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL, CASCADE)


class User(AbstractUser):
    name = CharField(max_length=256, null=True, blank=True)
    is_company = BooleanField(default=False)

    def __str__(self):
        return self.username

