from rest_framework.renderers import JSONRenderer


class SimpleJsonApi:
    renderer_classes = [JSONRenderer]
