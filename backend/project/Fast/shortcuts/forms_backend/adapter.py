from typing import Any


class RequestSessionStorage:

    def __init__(self, request):
        self.__request = request
    
    def get(self, name: str, value: Any = None):
        return self.__request.session.get(name, value)

    def set(self, name: str, value: Any, *trash):
        self.__request.session[name] = value

        