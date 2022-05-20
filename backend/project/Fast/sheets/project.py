from .django_class import Base
from .editor import Editor
from pathlib import Path
from time import sleep
from .support import *
import shutil as pc
import io


class DjangoProject(Base):
    def __init__(self, base_path: str, project: str):
        self.base_path = self.adapt_path(base_path)
        self.project = self.adapt_path(project)
        self.path = f'{self.base_path}/{self.project}'
        self.settings = Editor(self.path, 'settings.py')
        assert_folder_existence(self.path)
            
    def adapt_urls_py(self):
        editor = Editor(self.path, 'urls.py')
        imports = ['from django.conf import settings', 'from django.conf.urls.static import static', 'from django.urls import path, include']
        editor.replace_line('from django.urls', imports)  # new_reading
        url_conf = ['\n\nurlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)', 'urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)']
        editor.insert_code(']', url_conf)

    
    def move_to_origin(self, files_path):
        origin_path = Path(self.path).parent.parent
        for file in files_path.iterdir():
            file_path = Path(file)
            pc.move(file_path, origin_path)
    
    def insert_important_comments(self):
        inserts = [("DEFAULT_AUTO_FIELD", "\n\n# My settings"),
                   ("INSTALLED_APPS", f'{sp(4)}# Django apps'),
                   ("    'django.contrib.staticfiles'", f'{sp(4)}# My apps\n{sp(4)}# Others apps'),
        ]
        for current, new in inserts:
            self.settings.insert_code(current, new)

    def add_env_file(self):
        with io.open(f'{self.base_path}/.env', 'w') as file:
            pass
        editor = Editor(self.base_path, '.env')
        editor.add_in_start([
            'DEBUG=True',
            'SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxxxxx'
        ])
        
    def _settings_replaces(self):
        replaces = [
            (f"{sp(8)}'DIRS': [],", f"{sp(8)}'DIRS': [Path(BASE_DIR, 'frontend/templates')],"),
            ("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = 'pt-br'"),
            ("TIME_ZONE = 'UTC'", "TIME_ZONE = 'America/Sao_Paulo'"),
            ("DEBUG", "DEBUG = config('DEBUG', default=False, cast=bool)"),
        ]
        return replaces
        
    def _settings_inserts(self):
        settings = [
            "\nSTATICFILES_DIRS = [Path(BASE_DIR, 'frontend/static')]", 
            "STATIC_ROOT = Path('static')","MEDIA_ROOT = Path(BASE_DIR,'frontend/media')", 
            "MEDIA_URL = '/media/'", "ACCOUNT_SESSION_REMEMBER = True",
            "STATIC_PAGE_CACHE_TIMEOUT = 60*60*2"
        ]
        inserts = [
            ("# My settings", settings),
            #("", ""),
        ]
        return inserts
    
    def adapt_settings(self):
        replaces = self._settings_replaces()
        inserts = self._settings_inserts()
        
        for current, new in replaces:
            self.settings.replace_line(current, new)

        for current, new in inserts:
            self.settings.insert_code(current, new)

        self.settings.add_in_start(['from decouple import config'])
