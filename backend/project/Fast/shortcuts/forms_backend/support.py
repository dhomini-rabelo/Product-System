from django.core.cache import cache
from Fast.shortcuts.forms_backend.adapter import RequestSessionStorage


def get_attrs_by_type(request, form_type: str) -> dict:
    match form_type:
        case 'global':
            return {'storage': cache, 'update_function_name': 'load_form_with_values'}
        case 'dinamic':
            return {'storage': RequestSessionStorage(request), 'update_function_name': 'change_form_with_values'}


def create_form_settings(request, form_type: str, form_name: str, form_class) -> dict:
    form_settings = {
        'name': f'{form_name}_form',
        'fast_name': f'fast_{form_name}',
        'used_name': f'used_{form_name}',
        'class': form_class,
        **get_attrs_by_type(request, form_type),
    }

    return form_settings



def get_form_settings(request, form_type: str, form_name: str, form_class) -> dict:
    settings = request.session.get(f'{form_name}_settings', create_form_settings(request, form_type, form_name, form_class))
    return settings



base_changes = [('[name]', 'name'), ('[label]', 'label'), ('[placeholder]', 'placeholder')]
def construct_form(form_settings: dict, fields: list[dict], html_structure: str, changes=base_changes):
    page_form = form_settings['class']()
    page_form.add_fields(fields, html_structure, changes)
    return page_form



def save_base_form(form_settings, form):
    form_settings['storage'].set(form_settings["name"], form.form_for_save(), None)
    form_settings['storage'].set(form_settings["fast_name"], form.get_form(), None)


def save_used_form(request, form_settings, form):
    request.session[form_settings['used_name']] = form.get_form()


def save_form_values_and_form_errors(request, form_settings: str, fields_values: dict, errors: dict):
    conditions = {'fields': fields_values.keys() > 0, 'errors': errors.keys() > 0}
    if list(conditions.values()) == [False, False]: return

    page_form = form_settings['class']()
    form = form_settings['storage'].get(form_settings["name"])

    if conditions['fields']:
        update_form_with_values_function = getattr(page_form, form_settings['update_function_name'])
        update_form_with_values_function(form, fields_values)
    else:
        page_form.load_form(form)

    if conditions['errors']:
        page_form.show_errors(errors)

    save_used_form(request, form_settings, page_form)




def load_form_and_delete_used_form(request, form_settings: dict):
    used_form = request.session.get(form_settings["used_name"])
    
    if used_form is None:
        return form_settings['storage'].get(form_settings["fast_name"])
    else:
        request.session[form_settings["used_name"]] = None
        return used_form