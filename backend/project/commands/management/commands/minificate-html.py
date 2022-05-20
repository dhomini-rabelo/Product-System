from pathlib import Path
from ..comand import BasicCommand
from django.conf import settings
import requests
import io

    
class Command(BasicCommand):

    help = 'Minificate html'

    def add_arguments(self, parser):
        parser.add_argument('html_path', type=str)
        parser.add_argument('--use-default-path', '-u', action='store_true')
    
    def handle(self, *args, **options):
        path = f'{str(settings.BASE_DIR)}/frontend/templates'
        pages = 'pages/' if not options['use_default_path'] else ''
        archive = f'{pages}{options["html_path"].replace(".", "/")}.html'
        archive_path = f'{path}/{archive}'
        folders = archive.split('/')
        self.create_page_folders(path, [folder for i, folder in enumerate(folders) if i != len(folders) - 1])

        url = 'https://www.toptal.com/developers/html-minifier/raw'
        data = {'input': io.open(archive_path, 'r').read()}
        response = requests.post(url, data=data)

        self.create_minificated_archive(archive, response.text)
        self.show_actions([
            f'create minificated page in min/{archive}'
        ])

    def create_minificated_archive(self, archive_short_path, content):
        new_archive_path = f'{str(settings.BASE_DIR)}/frontend/templates/min/{archive_short_path}'
        with io.open(new_archive_path, 'w') as file:
            file.write(content)

    def create_page_folders(self, base_path: Path, folders: list[str]):
        path = ''
        for folder in folders:
            new_path = Path(base_path, 'min', f'{path}{folder}')
            try:
                new_path.mkdir()
            except FileExistsError:
                pass
            path += f'{folder}/'