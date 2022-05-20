from django.contrib import auth
from backend.accounts import User


def check_password(request, current_password: str, field_error: str):
    user = auth.authenticate(request, username=request.user.username, password=current_password)
    if user is not None:
        return {'status': 'valid', 'errors': {}}
    else:
        return {'status': 'invalid', 'errors': { field_error: 'Senha incorreta' }}


def change_password(request, new_password: str):
    user = request.user
    user.set_password(new_password)
    user.save()

def anonymous_change_password(username, new_password_value: str):
    user = User.objects.get(username=username)
    user.set_password(new_password_value)
    user.save()

