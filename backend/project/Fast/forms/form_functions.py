from .support import get_equal_fields_error, change_password
from ..utils.main import gets


def vf_equal_fields(errors: dict, new_errors: list, post_form: dict, equal_fields: list):
    for main, copy, error_message in equal_fields:
        copy_error = errors.get(copy)
        if copy_error is None:
            main_value, copy_value = gets(post_form, main, copy)
            equal_errors = get_equal_fields_error(main_value, copy_value, copy, error_message)
            new_errors.append(equal_errors)
            
            
def vf_change_password(errors: dict , new_errors: dict, post_form: dict, key_value):
        change_password_errors = change_password(post_form, **key_value)
        new_errors.append(change_password_errors)


validate_form_functions = {
    'equal_fields': vf_equal_fields,
    'change_password': vf_change_password,
}