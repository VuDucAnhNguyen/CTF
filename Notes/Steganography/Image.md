## Lý thuyết
### Ảnh .PNG
#### Cấu trúc
Ảnh PNG được chia thành các chunk dữ liệu, toàn bộ các trường dữ liệu số nguyên của PNG đều dùng định dạng Big-endian. Mỗi chunk dữ liệu có cấu trúc gồm các trường
| Trường | Số byte | Định dạng | Giải thích |
| --- |  ---------- | ------------- | ---- |
| Length | 4 | Số nguyên | Quy định số byte trường Chunk Data |
| Chunk Type | 4 | Mã ASCII | Định danh của chunk (VD: `IHDR`, `IDAT`,..) |
| Chunk Data | N | | Nội dung cấu hình hoặc pixel của ảnh |
| CRC | 4 | Hash value | Dùng kiểm tra các trường trước bị hỏng/ sửa hay không |

#### IHDR
Chunk đầu tiên trong file ảnh, chứa cấu hình của file ảnh và trường Length của chunk IHDR luôn cố định là 13 byte (`00 00 00 0D`)

| Vị trí byte | Ý nghĩa | Giải thích |
| --- |  ---------- | ------------- |
| Byte 1-4 | Width | Chiều rộng của ảnh |
| Byte 5-8 | Height	| Chiều cao của ảnh |
| Byte 9 | Bit Depth | Số bit quy định kênh màu (Giá trị hợp lệ: 1, 2, 4, 8, 16) |
| Byte 10 | Color Type |Hệ màu của ảnh: <br> • 0: Grayscale (Ảnh xám) <br> • 2: Truecolor / RGB (Ảnh màu) <br> • 3: Indexed-color (Bảng màu Palette - cần có chunk PLTE) <br> • 4: Grayscale với kênh Alpha <br> • 6: Truecolor với kênh Alpha (RGBA) |
| Byte 11	| Compression Method | Phương thức nén, bắt buộc là `0` |
| Byte 12	| Filter Method | Phương thức tiền xử lý bộ lọc hàng pixel trước khi nén, bắt buộc là `0` |
| Byte 13	| Interlace Method | Phương thức hiển thị ảnh quét dòng: <br> • 0: Không sử dụng (Quét từ trên xuống dưới) <br> • 1: Sử dụng Adam7 interlace (Ảnh hiện mờ rồi nét dần khi tải chậm) |

#### IDAT
Khối này chứa dữ liệu pixel thực tế của bức ảnh đã được đi qua bộ lọc và nén lại. FIle ảnh có thể bao gồm nhiều khối IDAT liên tiếp nhau để tiện truyền tin qua mạng.
#### IEND
Khối đánh dấu kết thúc file PNG

#### Một số chunk bổ trợ
- PLTE (Palette Chunk): Chứa bảng màu (chỉ bắt buộc khi Color Type trong IHDR bằng 3). Gồm chuỗi các cụm 3-byte đại diện cho hệ màu RGB

- tRNS (Transparency Chunk): Lưu thông tin về độ trong suốt của các pixel đối với ảnh không có kênh Alpha chuyên dụng (Hệ màu 0, 2, 3)

- gAMA (Gamma Chunk): Gồm 4 byte quy định tỷ lệ Gamma của màn hình nguồn giúp đồng bộ độ tương phản hiển thị trên các thiết bị khác nhau

- tEXt / zTXt (Textual Data Chunk): Chứa các chuỗi văn bản thuần túy dạng Key-Value giúp lưu trữ metadata
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
Kích thước hiển thị của ảnh bé hơn so với kiến thức thực tế, flag có thể được giấu vào phần không được hiển thị này. Cần lưu ý kiểm tra số byte dữ liệu thô trước và sau resize để có thể khớp nhau.

VD ảnh JPG: [Are ya wining, son?](../../Writeups/CIT_2026/Steganography/Are_ya_winning,_son/writeup.md)

VD ảnh PNG: [Triplets](../../Writeups/TJCTF_2026/Forensics/Triplets/writeup.md)


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

### Sử dụng Opensteg
VD: [Polar Fragment](../../Writeups/V1T_2026/Forensics/Polar_Fragment/writeup.md)

### Chèn byte xen giữa các byte của ảnh
Byte của file được giấu nằm xen giữa các byte ảnh. Thường được dùng cho các định dạng ảnh không nén (.bmp) do dữ liệu điểm ảnh pixel được lưu tuyến tính nên ảnh chỉ nhiễu chứ không hỏng như .png và .jpg

VD: [Invisible WORDs](../../Writeups/picoCTF/Invisible_WORDs/writeup.md)

### Sử dụng zsteg (dành cho .png và .bmp)
```
zsteg [file_name]
```

### LSB, color planes
flag có thể được giấu trong ảnh bằng cách thay đổi các bit cuối của các kênh màu dẫn nên khó có thể nhận ra bằng mắt thường

VD: [Cool car](../../Writeups/CIT_2026/Steganography/Cool_car/writeup.md)

### Kỹ thuật EMD (Exploiting Modification Direction)
Thay vì chỉ tác động vào một pixel độc lập (như phương pháp LSB truyền thống), EMD xem xét một nhóm gồm \(n\) pixel như một đơn vị và chỉ thay đổi tối đa một đơn vị giá trị của một pixel duy nhất trong nhóm đó để nhúng thông tin.

Nhóm pixel: Một nhóm gồm \(n\) pixel được ký hiệu là \((x_1, x_2, ..., x_n)\).

Hệ cơ số: EMD nhúng dữ liệu dưới dạng hệ cơ số \(2n+1\).

Công thức hàm trích xuất:

$$f(x_1, x_2, ..., x_n) = \left( \sum_{i=1}^{n} x_i \cdot i \right) \bmod (2n + 1)$$

VD: [Stegmaxxing](../../Writeups/BKISC_CTF_2026/Miscellaneous/Stegmaxxing/writeup.md)

### Stepic
Là một công cụ dòng lệnh bằng Python dùng để ẩn giấu văn bản hoặc dữ liệu vào trong một bức ảnh bằng cơ chế LSB
```
stepic -d -i [file_name]  
```

### Arnold's cat map
Kỹ thuật xáo ảnh bằng cách trượt pixel dựa vào công thức sau:
- công thức không tham số:
$$\begin{pmatrix} x_{n+1} \\ y_{n+1} \end{pmatrix} = \begin{pmatrix} 1 & 1 \\ 1 & 2 \end{pmatrix} \begin{pmatrix} x_n \\ y_n \end{pmatrix} \pmod 1$$

- công thức có tham số (a, b):
$$\begin{pmatrix} x_{n+1} \\ y_{n+1} \end{pmatrix} = \begin{pmatrix} 1 & a \\ b & ab + 1 \end{pmatrix} \begin{pmatrix} x_n \\ y_n \end{pmatrix} \pmod 1$$

VD: [RecoverMyPet](../../Writeups/scriptCTF_2026/Forensics/RecoverMyPet/writeup.md)