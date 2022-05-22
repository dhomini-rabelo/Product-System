from rest_framework.fields import empty
from abc import ABC


class AdaptDataSerializer:
    """
    This class adapts body data received

    require:
        self.adapt_data : FunctionType(data: body_data) => adapted_data
    """

    def __init__(self, instance=None, data=empty, **kwargs):
        obj_data = self.adapt_data(data)
        super().__init__(instance, obj_data, **kwargs)

    def run_validation(self, data=empty):
        obj_data = self.adapt_data(data)
        return super().run_validation(obj_data)