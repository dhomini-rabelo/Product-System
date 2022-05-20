# for utils

def get_name(text: str):
    list_string = text.split(' ')
    text = [word.strip().title() for word in list_string if word != '']
    return " ".join(text)

def get_only_numbers(text: str):
    new_text = ''
    for letter in text:
        if letter in list('0123456789'):
            new_text += letter
    return new_text


def get_decimal_from_money_br(text: str):
    new_text = ''
    for letter in text:
        if letter in list('0123456789,'):
            new_text += letter
    return new_text.replace(',', '.')        



filters_functions = {
    'strip': lambda text: text.strip(), 'name': lambda text: get_name(text),
    'only_numbers': lambda text: get_only_numbers(text),
    'money_br': lambda text: get_decimal_from_money_br(text),
    'none': lambda obj: obj,
}