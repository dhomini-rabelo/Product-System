from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.conf import settings



def cache_function(name: str, cache_timeout: int):
    def decorator_function(function):
        def wrapper_function(*args, **kwargs):
            if cache.get(name) is None:
                result = function(*args, **kwargs)
                cache.set(name, result, cache_timeout)
                return result
            return cache.get(name)
        return wrapper_function
    return decorator_function
