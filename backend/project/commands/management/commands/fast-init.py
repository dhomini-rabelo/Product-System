from Fast.sheets.project import DjangoProject
from Fast.sheets.eraser import delete_comments_by_folder
from ..comand import BasicCommand
from pathlib import Path
from django.conf import settings
from directory_tree import display_tree

    


class Command(BasicCommand):
    
    help = "Starting project with fast"

    def add_arguments(self, parser):
        parser.add_argument('--del', '-d', action='store_true')
        parser.add_argument('--compose', '-c', action='store_true')

    def handle(self, *args, **options):
        actions = [
            'creating folders for project',
            'inserting important comments for Fast',
            'changing  settings: - https://docs.djangoproject.com/en/4.0/ref/settings/',
            '   TEMPLATES["DIRS"], LANGUAGE_CODE, TIME_ZONE, STATICFILES_DIRS, STATIC_ROOT, MEDIA_ROOT',
            '   MEDIA_URL, ACCOUNT_SESSION_REMEMBER',
            'adapting archive urls.py',
            'adding env file - https://github.com/henriquebastos/python-decouple',
        ]
        
        self.create_project_folders(settings.BASE_DIR, options)
        
        if options['del']:
            actions.insert(1, 'deleting default coments')
            delete_comments_by_folder(str(settings.BASE_DIR), settings.PROJECT_NAME)

        project = DjangoProject(str(settings.BASE_DIR), settings.PROJECT_NAME)

        if options['compose']:
            actions.insert(2, 'Add Dockerfile and docker-compose - https://docs.docker.com/samples/django/')
            docker_files_path = Path(settings.BASE_DIR / 'commands/copies/docker')
            project.move_to_origin(docker_files_path)

        project.insert_important_comments()
        project.adapt_urls_py()
        project.add_env_file()
        project.adapt_settings()

        display_tree(str(settings.BASE_DIR))
        self.show_actions(actions)

    def create_project_folders(self, project_path: Path, options):
        folders = [
            'backend',
            'frontend',
            'frontend/static',
            'frontend/media',
            'frontend/static/styles',
            'frontend/static/styles/min',
            'frontend/static/styles/bases',
            'frontend/static/styles/pages',
            'frontend/static/styles/_compacts',
            'frontend/static/scripts',
            'frontend/static/scripts/min',
            'frontend/static/scripts/bases',
            'frontend/static/scripts/pages',
            'frontend/static/scripts/_compacts',
            'frontend/templates',
            'frontend/templates/_compacts',
            'frontend/templates/min',
            'frontend/templates/bases',
            'frontend/templates/pages',
            'test',
            'test/backend',
            'test/frontend',
            'test/e2e',
            'test/dependencies',
        ]

        for folder in folders:
            new_path = Path(project_path, folder)
            new_path.mkdir()