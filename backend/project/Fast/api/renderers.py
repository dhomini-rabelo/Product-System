from rest_framework.renderers import BrowsableAPIRenderer


class ApiWithoutFormRenderer(BrowsableAPIRenderer):

        def get_rendered_html_form(self, *args, **kwargs):
            return ''



class ApiWithoutRawDataFormRenderer(BrowsableAPIRenderer):

        def get_raw_data_form(self, *args, **kwargs):
            return ''



class ApiWithSimpleDRFView(BrowsableAPIRenderer):

        def get_raw_data_form(self, *args, **kwargs):
            return ''
        
        def get_rendered_html_form(self, *args, **kwargs):
            return ''
