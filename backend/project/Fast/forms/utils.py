from .checks import check_null
from .support import adapt_form_errors, adapt_list_of_post_form, convert_validation
from .functions_dict import other_errors_functions
from ..utils.main import gets
from django.db.models import Model



def get_post_form_errors(form: list, optional_fields: list[tuple]=[], choices: list[tuple]=[]) -> dict[str, str]:
    """
    Form list fields
    [
    [value, type, field_name, [(other_validation, *args),]],
    ]
    """
    # errors
    invalid_fields, none_fields, other_errors = [], [], []
    types_for_others_validations = [
        'unique', 'unique_m2m_or_custom','exists', 'only_str', 'only_numeric', 'email', 'caracters',
        'min-max-equal(length)', 'username', 'slug',
    ]
    
    for field, convert_var, name, more_validations in adapt_list_of_post_form(form):
        formated_field = convert_validation(field, convert_var)

        if check_null(field):
            none_fields.append(name)  
        elif str(formated_field) == 'convert_error':
            invalid_fields.append(name)
        else:
            for other_validation in more_validations:
                args = [*other_validation[1:]]
                args.insert(0, formated_field)
                validation = other_errors_functions[other_validation[0]]
                if not validation(*args):
                    other_errors.append([other_validation[0], name, args])
                    break
                
    form_errors = {'invalid_fields': invalid_fields, 'none_fields': none_fields,
                    'other_errors': other_errors}
    
    
    form_errors = adapt_form_errors(form_errors)

    for fields in choices:
        comparison = {}
        for field in fields:
            check = form_errors.get(field)
            comparison[field] = check if check is not None else 'none'
        errors_values = list(comparison.values())
        if (errors_values.count('Este campo é obrigatório') == (len(errors_values)-1)):
            for field in comparison.keys():
                if comparison[field] == 'Este campo é obrigatório':
                    optional_fields.append(field)


    for optional_field in optional_fields:
        optional_error = form_errors.get(optional_field)
        if (optional_error is not None) and (form_errors[optional_field] == 'Este campo é obrigatório'):
            del form_errors[optional_field]
        
    
    return form_errors if form_errors != {} else None



def validate_form_base(post_form, fields, default_type='str', default_validation=[('max_length', 256)]):
    def get_field(field):
        if isinstance(field, str):
            return field
        elif isinstance(field, list):
            return field[0]
    fields_name = list(map(get_field, fields)) 
    form_fields = gets(post_form, *fields_name)

    form_fields_adapted_format = []
    for index, field_format in enumerate(fields):
        field_adapted = []

        field_format = field_format if isinstance(field_format, list) else [field_format]

        match len(field_format):
            case 1:
                field_adapted = [form_fields[index], default_type, fields_name[index], default_validation]
            case 2:
                if isinstance(field_format[1], str):
                    field_adapted = [form_fields[index], field_format[1], fields_name[index], default_validation]
                elif isinstance(field_format[1], list):
                    field_adapted = [form_fields[index], default_type, fields_name[index], field_format[1]]
            case 3: 
                field_adapted = [form_fields[index], field_format[1], fields_name[index], field_format[2]]

        form_fields_adapted_format.append(field_adapted)

    errors = get_post_form_errors(form_fields_adapted_format)

    fields_value = {}

    for field in form_fields_adapted_format:
        fields_value[field[2]] = field[0]

    if errors is None:
        return {'status': 'valid', 'errors': {}, 'fields': fields_value}
    else:
        return {'status': 'invalid', 'errors': errors, 'fields': fields_value}
    
    
def check_and_change_image_field(request, field_name: str):
    new_file = request.FILES.get(field_name)
    if new_file:
        setattr(request.user, field_name, new_file)
        request.user.save()