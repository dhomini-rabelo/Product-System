from Fast.sheets.app import DjangoApp
from Fast.sheets.shortcuts import create_archives
from ..comand import BasicCommand
from django.conf import settings
from pathlib import Path
from directory_tree import display_tree


    


class Command(BasicCommand):

    help = 'Command for create fast app'
    
    def handle(self, *args, **options):
        # create folder
        new_app_path = Path(settings.BASE_DIR, 'backend', 'accounts')
        new_app_path.mkdir()
        self.create_app_folders(new_app_path)
        self.create_app_archives(new_app_path)
        app = DjangoApp(str(settings.BASE_DIR), f'backend/accounts', 'accounts', settings.PROJECT_NAME)
        app.create_url_archive()
        app.start_files()
        app.import_for_model()
        app.create_abstract_user_model()
        app.config_app()
        app.register_app()
        app.register_abstract_user()
        app.add_abstract_user_import()
        app.create_abstract_user_admin()
        app.create_abstract_user_forms()
        display_tree(str(new_app_path))
        self.show_actions(['create app', 'register app in settings.INSTALLED_APPS', 'setting settings.AUTH_USER_MODEL'])

    
    def create_app_folders(self, app_path: Path):
        folders = [
            'app',
            'app/migrations',
            'app/tests',
            'actions',
            'actions/functions',
            'actions/objects',
        ]
        for folder in folders:
            new_path = Path(app_path, folder)
            new_path.mkdir()

    def create_app_archives(self, app_path: Path):
        create_archives(app_path, [
            '__init__.py',
            'actions/functions/__init__.py',
            'actions/objects/__init__.py',
            'urls.py',
            'views.py',
            'app/__init__.py',
            'app/admin.py',
            'app/models.py',
            'app/forms.py',
            'app/tests/models.py',
            'app/tests/views.py',
            'app/migrations/__init__.py',
            'app/tests/__init__.py',
        ])


        

        