from .support import *
from .django_class import Base
from collections.abc import Mapping
from random import randint
from time import sleep
import io




class Editor(Base):
    
    def __init__(self, base_path: str, archive_path: str):
        self.base_path = self.adapt_path(base_path)
        self.archive_path = self.adapt_path(archive_path)
        self.path = f'{self.base_path}/{self.archive_path}'
        assert_file_existence(self.path)
        self.reading = self.read(self.path)
        self._adapt_list = lambda text_as_list: list(map(lambda line: f'{line}\n', text_as_list))
            
    def _get_line_position(self, code_line: str) -> int:
        for position, line in enumerate(self.reading):
            if code_line in line:
                return position + 1
        raise NotFoundError('Line not found')
        
        
    def add_in_start(self, text: Mapping[str, list]):
        if isinstance(text, str):
            text = [text]
        work_text = self._adapt_list(text) + self.reading[:]
        self._update(work_text)

    def add_in_end(self, text: Mapping[str, list]):
        if isinstance(text, str):
            text = [text]
        with io.open(self.path, 'a', encoding='utf-8') as script:
            for line in self._adapt_list(text):
                script.write(line)
        
        
    def replace_line(self, current: Mapping[str, int], new: Mapping[str, list]):
        if isinstance(current, str):
            line_number = self._get_line_position(current)
            self.replace_line(line_number, new)
        elif isinstance(current, int):
            current -= 1
            if isinstance(new, str):
                self.reading[current] = f'{new}\n'
            elif isinstance(new, list):
                self.reading = self.reading[:current] + self._adapt_list(new) + self.reading[current+1:]
            self._update(self.reading)
        
    def add_in_line(self, current: Mapping[str, int], new: str):
        line_number = self._get_line_position(current) if isinstance(current, str) else (current - 1)
        current_line = self.reading[line_number][:-1]
        self.replace_line(line_number, f'{current_line}{new}')

    def insert_code(self, line_code: Mapping[str, int], new: Mapping[str, list]):
        line_number = self._get_line_position(line_code) if isinstance(line_code, str) else (line_code - 1)
        if isinstance(new, str):
            self.reading.insert(line_number, f'{new}\n')
        elif isinstance(new, list):
            self.reading = self.reading[:line_number+1] + self._adapt_list(new) + self.reading[line_number+1:]         
        self._update(self.reading)

    def delete_line(self, line_code: Mapping[str, int]):
        line_number = self._get_line_position(line_code) if isinstance(line_code, str) else (line_code - 1)
        del self.reading[line_number]
        self._update(self.reading)
        
    def delete_many_lines(self, start: int, end: int):
        counter = 0
        for line_number in range(start, end+1):
            counter += 1
            del self.reading[line_number - counter]
        self._update(self.reading)
                    
    def _update(self, reading: list):
        sleep(0.5)
        with io.open(self.path, mode='w', encoding='utf-8') as code_file:
            start = 1 if reading[0] == '\n' else 0
            for line in reading[start:]:
                code_file.write(line)
        self.reading = reading


