from pathlib import Path
import io

def create_archives(path: Path | str, archives: list[str]):
    for arquive_name in archives:
        with io.open(f'{str(path)}/{arquive_name}', 'w') as file:
            pass
