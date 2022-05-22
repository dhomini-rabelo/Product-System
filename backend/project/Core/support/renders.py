from rest_framework.renderers import JSONRenderer

class SimpleRenderer:
    # must be a first father class
    renderer_classes = [JSONRenderer]