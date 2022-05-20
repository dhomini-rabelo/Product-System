from abc import ABC

class AppModels(ABC):

    def import_for_model(self):
        new_import = 'from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField, SET_NULL, CASCADE)'
        self.models.add_in_start(new_import)
    
    def create_abstract_user_model(self):
        imports =  [
            "from django.contrib.auth.models import AbstractUser", "from django.utils.safestring import mark_safe",
        ]
        abstract_user_class = [
            '\n\nclass User(AbstractUser):', 
            *self.spaces([
                "img = ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)\n",
                "def __str__(self):",
                *self.spaces([
                    "return self.username\n",         
                ], 4),             
            ], 4),
        ]
        self.models.add_in_start(imports)
        self.models.add_in_end(abstract_user_class)

                