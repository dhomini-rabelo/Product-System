# this module
from .functions_dict import filters_functions
# others
from datetime import datetime
from collections.abc import Mapping
from typing import Any

def simplification(obj_name: str):
    simplification = {'decimal.Decimal': 'decimal', 'datetime.date': 'date'}
    simplified_name = simplification.get(obj_name)
    if simplified_name is None:
        return obj_name
    else:
        return simplified_name


def get_type_name(obj: Any):
    str_type = str(type(obj))
    initial_position = str_type.find("'")
    end_position = str_type[initial_position+1:].find("'") + len(str_type[: initial_position+1])
    class_name = str_type[initial_position+1:end_position]
    return simplification(class_name)


def filters(field: Mapping[str, list], new_type: str = 'strip'):
    alloweds_new_types = ['strip', 'name', 'only_numbers', 'money_br', 'none']
    if isinstance(field, str):
        return filters_functions[new_type](field)
    elif isinstance(field, list):
        return list(map(lambda obj: filters_functions[new_type](obj), field))
    else:
        return field


def gets(post_obj: dict, *args, obj_filter='strip'):
    fields = list()
    for field in args:
        fields.append(filters(post_obj.get(field), obj_filter))
    return fields
    

def if_none(obj: Any, new_value: Any):
    if obj is None:
        return new_value
    return obj




def get_age(date: str):
    input_date = datetime.strptime(date, '%d/%m/%Y') 
    today_date = datetime.now()
    difference = today_date - input_date
    return int(difference.days/365.25)



def jsObj(keys: set[str], original_data: dict[str, str]):
    new_data = {}
    for key in keys:
        new_data[key] = original_data[key]
    return new_data
