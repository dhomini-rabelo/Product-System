from django.contrib import auth
from backend.accounts import User
from ...utils.main import gets



def login(request, user):
    auth.login(request, user)


def logout(request):
    auth.logout(request)


def validate_login(request, process: dict):
    user_type, password = gets(request.POST, process['type'], 'password')
    
    user_for_login = User.objects.filter(**{process['type']: user_type}).first()
    
    if user_for_login is None:
        return  {'status': 'invalid', 'errors': {process['type']: process['error_message']}}

    user = auth.authenticate(request, username=user_for_login.username, password=password)
    
    if user is not None:
        return {'status': 'valid', 'errors': {}, 'user': user}
    else:
        return {'status': 'invalid', 'errors': {'password': 'Senha incorreta'}}
