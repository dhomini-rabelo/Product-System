from .utils import validate_form_base
from .form_functions import validate_form_functions
from .support import update_errors, adapt_message_errors


def validate_form(post_form, form_object: dict):
    form_object['keys_order'] = form_object.get('keys_order') if form_object.get('keys_order') else []
    
    new_errors: list[dict] = []
    validation = validate_form_base(post_form, **form_object['form_base'])
    
    
    for other_validation in form_object['keys_order']:
        other_validation_function = validate_form_functions[other_validation]
        # args -> validation_errors: dict ,new_errors: dict, post_form: dict, key_value: Any
        other_validation_function(validation['errors'], new_errors, post_form, form_object[other_validation])
    
    
    new_errors = list(filter(lambda errors: errors != {}, new_errors))
    
    if len(new_errors) > 0:
        validation['status'] = 'invalid'
        update_errors(validation['errors'], new_errors)

    validation['errors'] = adapt_message_errors(validation['errors'], form_object.get('adapt_message_errors')) 
    
    return validation