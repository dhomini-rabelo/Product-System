from Support.Code.actions.Support.forms.form import BlockForm
from .loaded import loaded_forms
from Support.Code.actions.Support.utils.main import gets

    

def construct_form(form_name: str, fields:list[dict], blocks: dict) -> BlockForm:
    page_form = BlockForm()

    if form_name in loaded_forms.keys() and f'fast_{form_name}' in loaded_forms.keys():
        page_form.fast_load_form(loaded_forms[form_name], loaded_forms[f'fast_{form_name}'])
    else:
        page_form.load_blocks(blocks)
        page_form.add_fields(fields)
        
    return page_form


def delete_form(request, form_nickname: str):
    request.session[f'{form_nickname}_form_errors'] = None
    request.session[f'{form_nickname}_fields'] = None



def load_form(request, form_nickname: str, with_changes:bool=False) -> BlockForm:
    page_form = BlockForm()
    
    form_name = f'{form_nickname}_form'
    form_fields = f'{form_nickname}_fields'
    form_errors = f'{form_nickname}_form_errors'

    
    if request.session.get(form_fields) is None:
        page_form.fast_load_form(request.session[form_name], request.session[f'fast_{form_name}'])
    else:
        if request.session.get(form_errors) is None:
            if with_changes:
                page_form.change_form_with_values(request.session[form_name], request.session[form_fields])
            else:
                page_form.load_form_with_values(request.session[form_name], request.session[form_fields])
        else:
            if with_changes:
                page_form.change_form_with_values(request.session[form_errors], request.session[form_fields])
            else:
                page_form.load_form_with_values(request.session[form_errors], request.session[form_fields])

    delete_form(request, form_nickname)
    
    return page_form



def save_base_form(request, form_class: BlockForm, form_nickname: str):
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
        page_form = BlockForm()
        page_form.load_form(request.session[form_name])
        page_form.show_errors(errors)
        request.session[form_errors] = page_form.form_for_save()
    else:
        request.session[form_errors] = None
