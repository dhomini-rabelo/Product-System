from PIL import Image
from pathlib import Path



def resizer(archive, new_size):
    here = Path.cwd()
    img = Image.open(archive)
    l, h = img.size
    new_h = round((new_size * h) / l)
    new_image_path = here / Path(f'new/{archive}')
    new_image = img.resize((new_size, new_h), Image.LANCZOS)
    new_image.save(
        new_image_path,
        optimized=True,
        quality=75
    )
    img.close()
