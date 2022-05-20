# django
from django.core.validators import validate_slug, validate_unicode_slug 
from django.core.exceptions import ValidationError
from ..utils.functions_dict import get_name


def adapt_slug(slug: str):
    adapted_slug = ''
    replaces = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'â': 'a', 'ê': 'e', 'î': 'i', 'ô': 'o', 'û': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'ã': 'a', 'õ': 'o',
    }
    slug = slug.replace('_',' ').replace(' ','-').lower()
    for letter in list(slug):
        change = replaces.get(letter)
        if change is not None:
            adapted_slug += change
        else:
            adapted_slug += letter
    return adapted_slug



def set_slug(_slug: str):
    slug = _slug[:]
    slug = get_name(slug)
    invalid_letters = list()
    slug = adapt_slug(slug)
    slug_list = list(slug)
    for letter in slug_list:
        try:
            validate_slug(letter)
            validate_unicode_slug(letter)
        except ValidationError:
            invalid_letters.append(letter)
    for letter in invalid_letters:
        slug_list.remove(letter)
    return "".join(slug_list)
    
