import pathlib
import shutil
import random

TRAIN_PERCENT = 0.8
# create data dir
target_folder = pathlib.Path("data")
target_folder.mkdir(exist_ok=True)

images_folder = pathlib.Path("resize")
data_pair = list(map(
    lambda x: {'txt': str(x.parts[-1]),
               'img': str(x.parts[-1]).replace(".txt", ".jpg"),
               "file_no_ext": x.parts[-1].replace(".txt", ""),
               "path": x},
    list(images_folder.glob("*.txt"))
))
random.shuffle(data_pair)
data_count = int(len(data_pair) * TRAIN_PERCENT)
train, val = data_pair[0:data_count], data_pair[data_count:]
d_items = {
    "train": train,
    "val": val,
}
for key, items in d_items.items():
    p = target_folder / key
    p.mkdir(exist_ok=True)
    p_img = p / 'images'
    p_img.mkdir(exist_ok=True)
    p_label = p / 'labels'
    p_label.mkdir(exist_ok=True)
    for item in items:
        txt_path = p_label / item['txt']
        img_path = p_img / item['img']
        temp = images_folder / item['txt']
        shutil.copy(str(temp), str(txt_path))
        temp = images_folder / item['img']
        shutil.copy(str(temp), str(img_path))

