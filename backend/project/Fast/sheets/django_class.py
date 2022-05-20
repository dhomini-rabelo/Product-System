from .support import *
import io


class Base:
    
   
    @staticmethod
    def adapt_path(path: str):
        backslash = '\*'[0]
        if backslash in path:
            path.replace(backslash, '/')
        return path 
    
    @staticmethod
    def adapt_pyname(archive_name: str):
        if archive_name.endswith('.py'):
            return archive_name
        return f'{archive_name}.py'
    
    @staticmethod
    def adapt_htmlname(archive_name: str):
        if archive_name.endswith('.html'):
            return archive_name
        return f'{archive_name}.html'
    
    def read(self, archive: str):
        path = archive
        try:
            assert_file_existence(path)
        except FileNotFoundError:
            path = self.adapt_pyname(archive)
            assert_file_existence(path)
        with io.open(path, mode='r', encoding='utf-8') as code_file:
            code = code_file.readlines()
            return code
        

        