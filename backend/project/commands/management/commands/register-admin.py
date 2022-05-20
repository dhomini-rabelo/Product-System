from Fast.sheets.app import DjangoApp
from ..comand import BasicCommand
from django.conf import settings

    

class Command(BasicCommand):

    help = 'Compact html file losing extends django command'

    def add_arguments(self, parser):
        parser.add_argument('model_address', type=str)

    def handle(self, *args, **options):
        app_name, model_name = options['model_address'].split('.')
        app = DjangoApp(str(settings.BASE_DIR), f'backend/{app_name}', app_name, settings.PROJECT_NAME)
        app.register_admin(model_name)
        self.show_actions([
            f'register {model_name} in {app_name} app - https://docs.djangoproject.com/en/4.0/ref/contrib/admin/'
        ])
