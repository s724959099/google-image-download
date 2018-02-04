from PIL import Image
import pathlib

WIDTH = 1248
HEIGHT = 384


def resize_image(from_path, to_path):
    im = Image.open(from_path)
    nim = im.resize((WIDTH, HEIGHT))
    nim.save(to_path)


result_folder = pathlib.Path("resize")
result_folder.mkdir(exist_ok=True)

target_folder = pathlib.Path("images")
for item in target_folder.glob("*.jpg"):
    to_path = result_folder / item.parts[-1]
    resize_image(str(item), to_path)
