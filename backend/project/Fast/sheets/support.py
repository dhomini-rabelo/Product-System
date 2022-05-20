from time import sleep
from pathlib import Path
from .exceptions import *



def response(msg: str, wait=0, entity='Feedback'):
    """
    Função que mostra um feedback ao usuário 
    Args:
        msg (str): feedback que será mostrado
        wait (int, optional): tempo de espera para vários response não sejam executados juntos. Defaults to 0.
        entity (str, optional): "Entidade" que executa  a ação. Defaults to 'Feedback'.
    """
    sleep(wait)
    print(f'{entity} > [ {msg.lower()} ]')
    

def assert_file_existence(path: str):
    if not Path(path).exists():
        raise FileNotFoundError(f'O caminho "{path}" não foi encontrado')
    elif not Path(path).is_file():
        raise PathIsAFolderError(f'"{path}" é o caminho de uma pasta, nesta feature precisamos de um arquivo')


def assert_folder_existence(path: str):
    if not Path(path).exists():
        raise FileNotFoundError(f'O caminho "{path}" não foi encontrado')
    elif Path(path).is_file():
        raise PathIsAFileError(f'"{path}" é o caminho de um arquivo, nesta feature precisamos de uma pasta')
    
    
def sp(spaces: int):
    return " " * spaces
    