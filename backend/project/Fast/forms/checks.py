# django
from django.contrib import auth
# others
from typing import Any

    
def check_null(obj: Any):
    # check if object is null or none
    try:
        if obj is None:
            return True
        elif isinstance(obj, str) and obj.strip() == '':
            return True
        elif len(obj) == 0:
            return True
    except TypeError:
        pass
    return False



def checks_null(object_list: list):
    # check if object list contains a null object  or none object
    for obj in object_list:
        if check_null(obj):
            return True
    return False



def check_is_logged(request) -> bool:
    # checks if user is logged in from a request
    user = request.user
    return user.is_authenticated
