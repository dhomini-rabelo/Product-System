from abc import ABC
import io

class AppTests(ABC):
            
    def create_test_archive(self, test_name: str):
        name = f'test_{self.adapt_pyname(test_name)}'
        with io.open(f'{self.base_path}/Support/code/tests/{name}', 'w', encoding='utf-8') as arc:
            arc.write('from django.test import TestCase\n')
            self.response(f'Criando {name} na pasta tests')
            