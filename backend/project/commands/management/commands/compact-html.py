from pathlib import Path
from ..comand import BasicCommand
from django.conf import settings
import requests
import io

    

class Command(BasicCommand):

    help = 'Compact html file losing extends django command'

    def add_arguments(self, parser):
        parser.add_argument('html_path', type=str)

    def handle(self, *args, **options):
        self.base_path = f'{settings.BASE_DIR}/frontend/templates'
        argument_path = f'pages/{options["html_path"].replace(".", "/")}'
        path = f'{self.base_path}/{argument_path}.html'

        initial_read = self.get_reading_list(path)
        self.family = self.get_family(initial_read, path)[::-1]

        if len(self.family) == 1:
            reading = initial_read

        for index_, html_file_path in enumerate(self.family[:-1]):
            son_html_file_path = self.get_reading_list(self.family[index_+1])
            if index_ == 0:
                new_reading_update = self.replace_django_blocks_for_code(self.get_reading_list(html_file_path), son_html_file_path)
            else:
                new_reading_update = self.replace_django_blocks_for_code(reading, son_html_file_path)
            reading = new_reading_update[:]

        reading = self.get_includes_of_html_and_del_blocks(reading)
        compact_path = f'{self.base_path}/_compacts/{argument_path}.html'


        with io.open(compact_path, 'w') as file:
            file.writelines(reading)
        with io.open(compact_path, 'r') as file:
            html_text = file.read()


        url = 'https://www.toptal.com/developers/html-minifier/raw'
        data = {'input': html_text}
        response = requests.post(url, data=data)

        with io.open(compact_path, 'w') as file:
            file.write(response.text)

        self.show_actions([
            f'create compact page in /_compacts/{argument_path}.html',
        ])


    def get_reading_list(self, path: str):
        with io.open(path, 'r') as file:
            reading_list = file.readlines()
        return reading_list

    def get_family(self, reading_list: list[str], initial_path):
        family = [initial_path]
        check = self.get_extends_html(reading_list)
        
        if check is None:
            return family
        
        while check is not None:
            family.append(check)
            new_reading = self.get_reading_list(check)
            check = self.get_extends_html(new_reading)

        return family        

    def get_extends_html(self, reading_list: list[str]) -> str | None:
        first_line = reading_list[0].strip()
        if first_line.startswith(r'{% extends'):
            html_base_archive_path = first_line.split("'")[1]
            extends_html_path = f'{self.base_path}/{html_base_archive_path}'
            return extends_html_path

    def replace_django_blocks_for_code(self, current_reading_list: list[str], son_reading_list: list[str]):
        new_reading = []
        checked_blocks = []
        get_lines = True
        for line in current_reading_list:
            if r'{% endblock %}' in line.strip():
                get_lines = True
            if get_lines:
                new_reading.append(line)
            if (line.strip().startswith(r'{% block')) and (line.strip() not in checked_blocks):
                block_content = self.get_block_content(line.strip(), son_reading_list)
                new_reading += block_content
                if block_content != []:
                    get_lines = False
                checked_blocks.append(line.strip())
        return new_reading

    def get_block_content(self, block_line: str, son_reading_list: list[str]):
        block_content = []
        get_line = False
        process_counter = 1

        for line in son_reading_list:
            if line.strip() == block_line:
                get_line = True
            elif line.strip().startswith(r'{% block'):
                process_counter += 1
            elif  r'{% endblock %}' in line.strip():
                process_counter -= 1
                if process_counter == 0:
                    if get_line is True:
                        block_content.append(line)
                    get_line = False
            if get_line is True:
                block_content.append(line)

        return block_content

    def get_includes_of_html_and_del_blocks(self, reading):
        new_reading = []
        for line in reading:
            if line.startswith(r'{% include'):
                html_archive_path = line.split("'")[1]
                path = f'{self.base_path}/{html_archive_path}'
                html_archive_content = self.get_reading_list(path)
                new_reading += html_archive_content
            elif (not (r'{% endblock %}' in line.strip())) and (not (line.strip().startswith(r'{% block'))):
                new_reading.append(line)
        return new_reading
