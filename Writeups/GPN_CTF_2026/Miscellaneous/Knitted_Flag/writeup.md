## Knitted Flag
I got a new knitting machine to help me with the tablecloths for the restaurant but I accidentally dropped my flag into it. Can you help me unravel it?

## Giải
Sau khi tải về thì được `pattern.k` chứa ngôn ngữ Knitout – một ngôn ngữ mã máy tiêu chuẩn dùng cho các máy dệt. Trong đó:
- `;!knitout-2`: header
- `;;Carriers: 1 2 3 4 5 6`: sử dụng 6 ống dẫn sợi từ 1 đến 6
- `inhook`: ống dẫn sợi màu tương ứng từ vị trí nghỉ vào vùng làm việc của giường kim
- `tuck`: tạo hàng mũi dệt đầu tiên để làm móng, giữ cho miếng vải dệt không bị tuột khỏi kim
- `xfer` di chuyển mũi dệt
- `+`: di chuyển sang phải 
- `-`: di chuyển sang trái
- `f`: mặt trước
- `b`: mặt sau
- `1 - 20`: số hiệu kim
```
;!knitout-2
;;Carriers: 1 2 3 4 5 6 
inhook 1
inhook 2
inhook 3
inhook 4
inhook 5
inhook 6
tuck - f20 
tuck - f18 
tuck - f16 
tuck - f14 
tuck - f12 
tuck - f10 
tuck - f8 
tuck - f6 
tuck - f4 
tuck - f2 
tuck + f1 
...
```

Viết script thực hiện việc khâu này
``` python
import re
from PIL import Image
import math

# Định nghĩa bảng màu (ở đây chọn chung 1 màu trắng để nổi đường khâu trên nền đen và đỡ rối mắt)
COLORS = {
    1: (255, 255, 255),  # Trắng
    2: (255, 255, 255),        
    3: (255, 255, 255),      
    4: (255, 255, 255),      
    5: (255, 255, 255),      
    6: (255, 255, 255)     
}

# 1. Đọc và phân tích dữ liệu dệt
knit_data = []
with open("pattern.k", "r") as f:
    lines = f.readlines()

for line in lines:
    line = line.strip()
    
    # Tìm lệnh 'knit'. Định dạng: knit [direction] [bed][needle] [carrier]
    match = re.match(r"knit\s+([+-])\s+([fb])(\d+)\s+(\d+)", line)
    if match:
        direction, bed, needle_idx, carrier = match.groups()
        # Chỉ xử lý các đường khâu mặt trước
        if bed == 'f':
            knit_data.append((int(needle_idx), int(carrier)))

# 2. Xây dựng ma trận dệt liên tục
# Xác định phạm vi kim (từ f1 đến f20)
min_needle = 1
max_needle = 20
width = max_needle - min_needle + 1

# Tạo một hình ảnh dài, mỏng chứa tất cả các mũi dệt mỗi hàng chỉ chứa 1 điểm ảnh tương ứng với kim được dệt
raw_image_data = []
for needle_idx, carrier in knit_data:
    row = [0] * width # Nền mặc định màu đen
    target_x = needle_idx - min_needle
    row[target_x] = carrier
    raw_image_data.append(row)

# 3. Chuyển đổi dữ liệu thô thành hình ảnh lưới và phóng to
height = len(raw_image_data)
raw_img = Image.new("RGB", (width, height))

for i in range(height):
    for j in range(width):
        carrier = raw_image_data[y][x]
        raw_img.putpixel((j, i), COLORS.get(carrier, (0, 0, 0)))

# Phóng to ảnh
final_width = width * 20
final_height = height
flag_img = raw_img.resize((final_width, final_height), Image.Resampling.NEAREST)

flag_img.save("flag.png")
```

Chạy script thì được flag là phần không có đường chỉ
![image](flag.png)

FLAG: **GPNCTF{con6ratU14TIOns_Y0u_H4V3_UndEr57o0d_kniTOuT_aND_uNRAV3leD_tH3_tabLEcLo7H5}**
