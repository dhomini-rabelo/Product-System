# django
from ...utils.main import if_none
from .support import get_success_message, get_error_message
from .exceptions import MessageTypeNotFoundError


def save_message(request, message_obj: dict):
    # message_obj -> title: str, message: str, type: str
    request.session['messages'] = if_none(request.session.get('messages'), {})
    request.session['messages'][message_obj['title']] = message_obj.copy()
    request.session.save()


def load_message(request, message_title):
    request.session['messages'] = if_none(request.session.get('messages'), {})
    if message_title in request.session['messages'].keys():
        match request.session['messages'][message_title]['type']:
            case 'success':
                message = get_success_message(request.session['messages'][message_title]['message'].upper())
            case 'error':
                message = get_error_message(request.session['messages'][message_title]['message'].upper())
            case _:
                raise MessageTypeNotFoundError('Type message not found')
        del request.session['messages'][message_title]
        return message
    return ''


def load_messages(request, *messages_title):
    messages = []
    for message_title in messages_title:
        new_message = load_message(request, message_title)
        messages.append(new_message)
    return messages


def save_many_messages(request, message_obj: dict):
    # message_obj -> title: str, messages_list: list[message: str, type: str]
    request.session['many_messages'] = if_none(request.session.get('many_messages'), {})
    request.session['many_messages'][message_obj['title']] = message_obj.copy()
    request.session.save()


def load_many_messages(request, message_title):
    request.session['many_messages'] = if_none(request.session.get('many_messages'), {})
    if message_title in request.session['many_messages'].keys():
        messages = []
        for message, message_type in request.session['many_messages'][message_title]['message_list']:
            match message_type:
                case 'success':
                    messages.append(get_success_message(message))
                case 'error':
                    messages.append(get_error_message(message))
                case _:
                    raise MessageTypeNotFoundError('Type message not found')
        del request.session['many_many_messages'][message_title]
        return messages
    return []