from .support import construct_form, get_form_settings, save_base_form, load_form, save_form_values_and_form_errors, delete_form
from django.core.cache import cache
from ...forms.form import Form



def get_form(request, form_nickname: str, form_data: dict, is_dinamic: bool = False, many: bool = False, form_class=Form):
    
    form_settings = get_form_settings(request, form_nickname, is_dinamic, many, form_class)
    storage = request.session if form_settings['type'] != 'basic' else cache
    
    if storage.get(form_settings['name']) is None:
        form = construct_form(form_settings, **form_data)
        save_base_form(request, form, form_nickname)
    else:
        form = load_form(request, form_nickname)

    return form.get_form()


def save_form(request, form_nickname: str, fields_values: dict, errors: dict):
    save_form_values_and_form_errors(request, form_nickname, fields_values, errors)
    
    
def delete_used_form(request, form_nickname: str):
    delete_form(request, form_nickname)
    