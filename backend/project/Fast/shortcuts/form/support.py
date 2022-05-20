from django.core.cache import cache
from ...forms.form import Form
from ...utils.main import gets, if_none
    

base_changes = [('[name]', 'name'), ('[label]', 'label'), ('[placeholder]', 'placeholder')]
def construct_form(form_settings: dict, fields: list[dict], html_structure: str, changes=base_changes) -> Form:
    page_form = form_settings['class']()

    page_form.add_fields(fields, html_structure, changes)
    cache.set(form_settings["name"], page_form.form_for_save(), None)
    cache.set(f'fast_{form_settings["name"]}', page_form.fast_load_form(), None)
        
    return page_form


def delete_form(request, form_nickname: str):
    request.session[f'{form_nickname}_form_errors'] = None
    request.session[f'{form_nickname}_fields'] = None



def load_form(request, form_nickname: str) -> Form:
    page_form = Form()
    
    form_name = f'{form_nickname}_form'
    form_fields = f'{form_nickname}_fields'
    form_errors = f'{form_nickname}_form_errors'

    
    if request.session.get(form_fields) is None:
        page_form.fast_load_form(request.session[form_name], request.session[f'fast_{form_name}'])
    else:
        if request.session.get(form_errors) is None:
            page_form.load_form_with_values(request.session[form_name], request.session[form_fields])
        else:
            page_form.load_form_with_values(request.session[form_errors], request.session[form_fields])

    delete_form(request, form_nickname)
    
    return page_form



def save_base_form(request, form_class: Form, form_nickname: str):
    request.session[f'{form_nickname}_form'] = form_class.form_for_save()
    request.session[f'fast_{form_nickname}_form'] = form_class.form


def save_form_values_and_form_errors(request, form_nickname: str, fields_values: dict, errors: dict):
    
    form_name = f'{form_nickname}_form'
    form_fields = f'{form_nickname}_fields'
    form_errors = f'{form_nickname}_form_errors'
    

    if fields_values != {}:
        request.session[form_fields] = fields_values
    else:
        request.session[form_fields] = None

    if errors != {}:
        page_form = Form()
        page_form.load_form(request.session[form_name])
        page_form.show_errors(errors)
        request.session[form_errors] = page_form.form_for_save()
    else:
        request.session[form_errors] = None


def get_form_type(is_dinamic: bool, many: bool) -> str:
    match [is_dinamic, many]:
        case [True, True]:
            return 'complex'
        case [False, False]:
            return 'basic'
        case [True, False]:
            return 'dinamic'
        case _:
            raise ValueError(f'Form type nt found')


def create_form_settings(form_name: str, is_dinamic: bool, many: bool, form_class) -> dict:
    form_settings = {
        'name': f'{form_name}_form',
        'fast_name': f'fast_{form_name}',
        'used_name': f'used_{form_name}',
        'type': get_form_type(is_dinamic, many),
        'class': form_class
    }

    return form_settings



def get_form_settings(request, form_name: str, is_dinamic: bool, many: bool, form_class) -> dict:
    settings = request.session.get(f'{form_name}_settings', create_form_settings(form_name, is_dinamic, many, form_class))
    return settings
