## Chromatic
### Đề bài
Red.

### Giải
Sau khi tải về thì được `chromatic.mp4` là video dài 54 giấy với chỉ một màu đỏ đổi độ đâm nhạt. Thử trích xuất các frame ảnh ra thì thấy mỗi 30 frame sẽ đổi màu một lần, các giá trị màu g, b = 0 còn các giá trị màu đỏ chính là ký tự ascii. Viết script trích xuất
```
from PIL import Image
import subprocess, sys

proc = subprocess.Popen(
    ["ffmpeg", "-i", "chromatic.mp4", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
)

W, H = 1280, 720
frame_size = W * H * 3

frames = []
while chunk := proc.stdout.read(frame_size):
    frames.append(chunk[0])

flag_string = ""

for i in range(len(frames) // 30):
    frame_index = i * 30
    flag_string += chr(frames[frame_index])

print(flag_string)
```

FLAG: **byuctf{It's_all_red_I_really_thought_it_would_be_more}**