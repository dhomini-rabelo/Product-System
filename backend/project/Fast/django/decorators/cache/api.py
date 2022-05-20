from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.conf import settings
from rest_framework.response import Response


def global_cache_page(cache_timeout: int):
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.get_path()) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.get_path(), response.data, cache_timeout)
                return response
            return Response(cache.get(request.get_path()))
        return wrapper_function
    return decorator_function


def double_cache_page(cache_timeout: int):
    def decorator_function(view_function):
        @cache_page(cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.get_path()) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.get_path(), response.data, cache_timeout)
                return response
            return Response(cache.get(request.get_path()))
        return wrapper_function
    return decorator_function


def super_cache_page(global_cache_timeout: int, browser_cache_timeout: int):
    def decorator_function(view_function):
        @cache_page(browser_cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.get_path()) is None:
                response = view_function(*args, **kwargs)
                cache.set(request.get_path(), response.data, global_cache_timeout)
                return response
            return Response(cache.get(request.get_path()))
        return wrapper_function
    return decorator_function


def static_page(view_function):
    @cache_page(settings.STATIC_PAGE_CACHE_TIMEOUT)
    def wrapper_function(*args, **kwargs):
        request = args[0]
        if cache.get(request.get_path()) is None:
            response = view_function(*args, **kwargs)
            cache.set(request.get_path(), response.data, None)
            return response
        return Response(cache.get(request.get_path()))
    return wrapper_function


def renew_or_cache_page(cache_timeout):
    def decorator_function(view_function):
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if request.headers.get('renew'):
                return view_function(*args, **kwargs)
            return cache_page(cache_timeout)(view_function)(*args, **kwargs)
        return wrapper_function
    return decorator_function


def control_cache_page(cache_timeout: int = 60*60*2):
    def decorator_function(view_function):
        @renew_or_cache_page(cache_timeout)
        def wrapper_function(*args, **kwargs):
            request = args[0]
            if cache.get(request.get_path()) is None or request.headers.get('renew') == settings.SECRET_KEY:
                response = view_function(*args, **kwargs)
                cache.set(request.get_path(), response.data, None)
                return response
            return Response(cache.get(request.get_path()))
        return wrapper_function
    return decorator_function
    