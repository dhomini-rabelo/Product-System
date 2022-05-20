from django.core.cache import cache


def renew_global_cache(url):
    cache.set(url, None, None)
