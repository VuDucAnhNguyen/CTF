## RecoverMyPet
### Đề bài
this is all i have left.

### Giải
Đề bài cho 36 ảnh có tên dạng `a_b.png` với a và b là 2 số nguyên tố cùng nhau. Kiểm tra exiftool 1 ảnh có description như sau:
```
ExifTool Version Number         : 13.50
File Name                       : 1_1.png
Directory                       : .
File Size                       : 768 bytes
File Modification Date/Time     : 2026:07:09 08:36:14-04:00
File Access Date/Time           : 2026:07:08 18:43:14-04:00
File Inode Change Date/Time     : 2026:08:12 01:52:54-04:00
File Permissions                : -rw-r--r--
File Type                       : PNG
File Type Extension             : png
MIME Type                       : image/png
Image Width                     : 60
Image Height                    : 60
Bit Depth                       : 8
Color Type                      : RGB
Compression                     : Deflate/Inflate
Filter                          : Adaptive
Interlace                       : Noninterlaced
Exif Byte Order                 : Big-endian (Motorola, MM)
Image Description               : i once had a cat, u know. but this crazy scientist took my cat and turned it into a donut 489 times and i cant find my cat anymore! (1/3)
Image Size                      : 60x60
Megapixels                      : 0.004
```

mỗi ảnh là một mảnh sử dụng kỹ thuật xáo ảnh Arnold's cat map với `donut X times` là số lần xáo, (A/B) là vị trí của ảnh để ghép các mảnh thành ảnh hoàn chỉnh, viết script thực hiện đảo ngược biến đổi và ghép các mảnh
``` python
from PIL import Image
import numpy as np
import os
import re

image_size = 60
grid_size = 6
tiles = {}

def exiftool(path):
    img = Image.open(path)
    exif_bytes = img.info.get("exif")
    text = exif_bytes.decode("latin1")
    match = re.search(r"donut (\d+) times.*?\((\d+)/(\d+)\)", text)
    X, A, B = map(int, match.groups())

    return X, A, B

def inverse(arr, a, b, times):
    result = arr.copy()
 
    idx = np.indices((image_size, image_size))
    row_idx, col_idx = idx[0], idx[1]
 
    xs, ys = col_idx, row_idx
 
    for _ in range(times):
        new_xs = ((a * b + 1) * xs - a * ys) % image_size
        new_ys = (-b * xs + ys) % image_size
 
        inverse_result = np.zeros_like(result)
        inverse_result[new_ys, new_xs] = result[ys, xs]
        result = inverse_result
 
    return result

for fname in sorted(os.listdir('./images')):
    if not fname.endswith(".png"):
        continue

    path = os.path.join('./images', fname)

    name = fname[:-4]
    a_str, b_str = name.split("_")
    a, b = int(a_str), int(b_str)

    X, A, B = exiftool(path)

    arr = np.array(Image.open(path).convert("RGB"))
    decoded = inverse(arr, a, b, X)
 
    tiles[(A, B)] = decoded
    print(f"{fname}: a={a}, b={b}, X={X}, position=({A},{B})")

canvas = Image.new("RGB", (image_size * grid_size, image_size * grid_size))
for (A, B), tile_arr in tiles.items():
    tile_img = Image.fromarray(tile_arr)
    canvas.paste(tile_img, ((B - 1) * image_size, (A - 1) * image_size))
 
out_path = "./flag_recovered.png"
canvas.save(out_path)
```

Sau khi chạy thì được ảnh hoàn chỉnh
![image](flag_recovered.png)

FLAG: **scriptCTF{w@t_4_cu71e_p@too1$}**