from abc import ABC
from ..editor import Editor

class AppForms(ABC):

    def create_abstract_user_forms(self):
        form = Editor(self.path, r'app\forms.py')
        imports = [
            'from django.contrib.auth import forms',
            'from .models import User',
        ]
        user_forms = [
            '\nclass UserChangeForm(forms.UserChangeForm):',
            *self.spaces([
                'class Meta(forms.UserChangeForm.Meta):',
                *self.spaces([
                    'model = User'
                ], 4)
            ], 4),
            '\nclass UserCreationForm(forms.UserCreationForm):',
            *self.spaces([
                'class Meta(forms.UserCreationForm.Meta):',
                *self.spaces([
                    'model = User'
                ], 4)
            ], 4),
        ]
        form.add_in_start(imports)
        form.add_in_end(user_forms)