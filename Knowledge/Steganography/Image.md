## Lý thuyết
### Ảnh .PNG

### Ảnh .JPEG
Marker `FF D8` bắt đầu của ảnh JPEG

Marker `FF C0` đánh dấu khối SOF0 (Start of Frame 0) chứa các thông số kỹ thuật:
| Vị trí byte | Ý nghĩa | Giải thích |
| --- |  ---------- | ------------- |
| Byte 1-2 | Length | Độ dài của khối SOF0 (thường là `00 11`) |
| Byte 3 | Precision	| Độ chính xác của mẫu màu (thường là `08` cho 8-bit) |
| Byte 4-5 | Height | Chiều cao của ảnh (big endian) |
| Byte 6-7 | Width | Chiều rộng của ảnh (big endian) |
| Byte 8	| Components | Số kênh màu (thường là `03` cho RGB) |

Marker `FF D9` kết thúc của ảnh JPEG

## Các phương pháp và công cụ ẩn tin trong ảnh
### Thay đổi kích thước hiển thị của ảnh
Kích thước hiển thị của ảnh bé hơn so với kiến thức thực tế, flag có thể được giấu vào phần không được hiển thị này

VD: https://github.com/VuDucAnhNguyen/CTF/blob/main/Writeups/CIT_2026/Steganography/Are_ya_winning%2C_son/writeup.md

### Sử dụng steghide/ stegseek
file có thể được giấu sử dụng `steghide` nhưng sẽ cần passphrase để có thể trích xuất
```
steghide --extract -sf [file_name]
```
<br>

passphrase này có thể bruteforce sử dụng `stegseek`
```
stegseek --crack [file_name] rockyou.txt
```
### Chèn byte xen giữa các byte của ảnh
Byte của file được giấu nằm xen giữa các byte ảnh. Thường được dùng cho các định dạng ảnh không nén (.bmp) do dữ liệu điểm ảnh pixel được lưu tuyến tính nên ảnh chỉ nhiễu chứ không hỏng như .png và .jpg

VD: https://github.com/VuDucAnhNguyen/CTF/blob/main/Writeups/picoCTF/Invisible_WORDs/writeup.md

### Sử dụng zsteg (dành cho .png và .bmp)
```
zsteg [file_name]
```