# django
from django.contrib.auth.models import AbstractUser
# this module
from .functions_dict import messages_form_errors, convert_functions
from ..utils.main import gets
# others
from decimal import InvalidOperation
from typing import Any





def update_errors(current_errors: dict, new_errors: list[dict]):
    new_errors_copy = [item.copy() for item in new_errors]
    for new_error_obj in new_errors_copy:
        for error_key in new_error_obj.keys():
            if current_errors.get(error_key) is None:
                current_errors[error_key] = new_error_obj[error_key]
                
                
def adapt_message_errors(error_messages: dict, new_error_messages: dict[list[str, str]] | None) -> dict:
    errors_obj = error_messages.copy()
    
    if new_error_messages is None:
        return errors_obj
    
    for error_key in new_error_messages.keys():
        if error_key in errors_obj.keys():
            for error_message, new_error_message in new_error_messages[error_key]:
                current_error_message = errors_obj[error_key]
                if current_error_message == error_message:
                    errors_obj[error_key] = new_error_message
            
    return errors_obj
    

    
def get_equal_fields_error(main: str, copy: str, key_for_error: str, error_message: str) -> dict:
    return {} if main == copy else {key_for_error: error_message}


def change_password(post_form: dict, user: AbstractUser, current_password: str, new_password: str, confirm_new_password: str) -> dict:
    errors = {}
    
    current_password_value, new_password_value, confirm_new_password_value = gets(post_form, current_password, new_password, confirm_new_password)
    

    errors[confirm_new_password] = get_equal_fields_error(new_password_value, confirm_new_password_value, 'As novas senhas são diferentes')
    
    if not user.check_password(current_password_value):
        errors[current_password] = 'Senha incorreta'
    else:
        if errors[confirm_new_password] == {}:
            user.set_password(new_password)
            user.save()

    return errors



    

def adapt_form_errors(form_errors: dict[str, list]) -> dict[str, str]:
    response = dict()
    for name in form_errors['invalid_fields']:
        response[name] = 'Este campo é inválido'
    for name in form_errors['none_fields']:
        response[name] = 'Este campo é obrigatório'
    for error, name, args in form_errors['other_errors']:
        if error in ['min_length', 'equal_length', 'max_length']:
            response[name] = messages_form_errors[error](args[1])
        else:
            response[name] = messages_form_errors[error]
    return response



def adapt_list_of_post_form(post_form_list: list):
    new_list = []
    for form_list in post_form_list:
        if len(form_list) == 3:
            model = form_list[:]
            model.append([])
            new_list.append(model)
        else:
            new_list.append(form_list)
    return new_list



def convert(obj: str, new_type: str):
    convert_process = convert_functions[new_type]
    
    if obj is not None:
        return convert_process(obj)
    else:
        return None



def convert_validation(field: Any, new_type: str):
    if new_type == 'pass': return 'valid'
    try:
        validation = convert(field, new_type)
        return validation if validation is not None else 'convert_error'
    except (ValueError, InvalidOperation):
        return 'convert_error'