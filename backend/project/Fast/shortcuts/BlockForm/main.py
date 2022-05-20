from .support import construct_form, save_base_form, load_form, save_form_values_and_form_errors, delete_form


def get_block_form(request, form_nickname: str, form_data: dict, use_history:bool=False):
    
    form_name = f'{form_nickname}_form'
    
    if request.session.get(form_name) is None:
        form = construct_form(form_name, **form_data)
        save_base_form(request, form, form_nickname)
    else:
        form = load_form(request, form_nickname, use_history)

    return form.get_form()


def adapt_form_with_history(form_data: dict, values: list[dict]):
    for index, value in enumerate(values):
        form_data['fields'][index].update(value.copy())


def save_block_form(request, form_nickname: str, fields_values: dict, errors: dict):
    save_form_values_and_form_errors(request, form_nickname, fields_values, errors)
    
    
def delete_used_block_form(request, form_nickname: str):
    delete_form(request, form_nickname)
    
def delete_base_block_form(request, form_nickname: str):
    request.session[f'{form_nickname}_form'] = None
    request.session[f'fast_{form_nickname}_form'] = None
    
    