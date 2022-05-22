from rest_framework.fields import empty


class AdaptDataSerializer:
    # require self.adapt_data
    def __init__(self, instance=None, data=empty, **kwargs):
        obj_data = self.adapt_data(data)
        super().__init__(instance, obj_data, **kwargs)

    def run_validation(self, data=empty):
        obj_data = self.adapt_data(data)
        return super().run_validation(obj_data)