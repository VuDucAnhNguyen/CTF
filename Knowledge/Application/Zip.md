## File .zip
### Cấu trúc 
#### Tổng quát
Cấu trúc của một file ZIP được thiết kế theo dạng tuyến tính (linear), cho phép ghi hoặc trích xuất dữ liệu một cách tuần tự và hỗ trợ khôi phục dữ liệu ngay cả khi file bị hỏng một phần.
|Khối | Thành phần | Chức năng |
| - | - | - |
|Khối dữ liệu tệp tin tuần tự  <br> (Local File Entries) | Local file header | chứa metadata (magic number, phiên bản zip, phương thức nén, tên tệp, thời gian sửa đổi, kích thước trước và sau nén và các trường mở rộng) |
| |  File data | phần dữ liệu sau nén |
| | Data descriptor | (tùy chọn) được dùng để ghi kích thước hoặc mã CRC-32 sau phần dữ liệu khi mà kích thước hoặc mã CRC-32 chưa được xác định lúc ghi header |
| Các khối bản ghi phụ trợ | Archive decryption header | Xuất hiện khi file zip được mã hóa, nó chứa thông tin xác thực và giải mã|
| | Archive extra data record | Dùng để lưu trữ thêm các thông tin bổ sung có cấu trúc |
| Thư mục trung tâm <br> (Central Directory) | | Đóng vai trò là bảng mục lục index, chứa danh sách file trong archive (có cả quyền truy cập, thuộc tính os, con trỏ đến Local file header) |

#### Local file header
```
          0x0  0x1  0x2  0x3│ 0x4  0x5│ 0x6  0x7│ 0x8  0x9│ 0xa  0xb│ 0xc  0xd│ 0xe  0xf
       ┌────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┐
0x0000 │     Signature      │ Version │  Flags  │Compress │Mod time │Mod date │ Crc-32  │
       ├──────────┬─────────┴─────────┼─────────┴─────────┼─────────┼─────────┼─────────┤
0x0010 │ (Crc-32) │  Compressed size  │ Uncompressed size │Fname len│Extra len│         │
       ├──────────┴───────────────────┴───────────────────┴─────────┴─────────┴─────────┤
0x0020 │ File name (Variable size)                                                      │
       ├────────────────────────────────────────────────────────────────────────────────┤
0x0030 │ Extra field (Variable size)                                                    │
       └────────────────────────────────────────────────────────────────────────────────┘
```

#### Data descriptor
```
          0x0  0x1  0x2  0x3│ 0x4  0x5  0x6  0x7│ 0x8  0x9  0xa  0xb
       ┌────────────────────┼───────────────────┼───────────────────┐
0x0000 │       Crc-32       │  Compressed size  │ Uncompressed size │
       └────────────────────┴───────────────────┴───────────────────┘
```

#### Central directory
- file header:
```
          0x0  0x1  0x2  0x3  │ 0x4  0x5│ 0x6  0x7│ 0x8  0x9│ 0xa  0xb│ 0xc  0xd│ 0xe  0xf
       ┌──────────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼─────────┐
0x0000 │Signature (PK\x01\x02)│ Version │Vers need│  Flags  │Compress │Mod time │Mod date │
       ├──────────────────────┼─────────┴─────────┼─────────┴─────────┼─────────┼─────────┤
0x0010 │        Crc-32        │  Compressed size  │ Uncompressed size │Fname len│Extra len│
       ├──────────┬───────────┼─────────┬─────────┴───────────────────┼─────────┴─────────┤
0x0020 │Comm len  │Disk start │Int attr │      External attr.         │Offset of loc hdr  │
       ├──────────┴───────────┴─────────┴─────────────────────────────┴───────────────────┤
0x0030 │ File name (Variable size)                                                        │
       ├──────────────────────────────────────────────────────────────────────────────────┤
0x0040 │ Extra field (Variable size)                                                      │
       ├──────────────────────────────────────────────────────────────────────────────────┤
0x0050 │ File comment (Variable size)                                                     │
       └──────────────────────────────────────────────────────────────────────────────────┘
```

- end of file
```
          0x0  0x1  0x2  0x3  │ 0x4  0x5│ 0x6  0x7│ 0x8  0x9│ 0xa  0xb│ 0xc  0xd  0xe  0xf
       ┌──────────────────────┼─────────┼─────────┼─────────┼─────────┼───────────────────┐
0x0000 │Signature (PK\x01\x02)│Disk num │Disk w/cd│Disk entr│Totl entr│Central direct size│
       ├──────────────────────┼─────────┴─────────┴─────────┴─────────┴───────────────────┤
0x0010 │Offset of cd wrt stk  │Comm len │ .ZIP file comment (Variable size)               │
       └──────────────────────┴─────────┴─────────────────────────────────────────────────┘
```

### Thuật toán nén
- Store: File không được nén
- Deflate: Sử dụng LZ77 + Huffman coding, nhanh và hiệu quả, là thuật toán nén mặc định của zip
- Deflate64: phiên bản cải thiện của Deflate nhưng độ tuơng thích và hỗ trợ hạn chế
- BZIP2: khả năng nén tốt hơn nhờ dùng Burrows-Wheeler transform nhưng tốc độ nén chậm hơn chậm hơn Deflate
- LZMA: Tỷ lệ nén cao nhưng tốn nhiều tài nguyên khi nén, là lõi cho 7z
- PPMd - Statistical compression tốt cho text nhưng chậm và tốn RAM

### Mã hóa
-  ZipCrypto (Traditional PKZIP Encryption)
    - phương pháp mã hóa cũ
    - yếu và có thể bẻ khóa
    - Có lỗ hổng known-plaintext attacks
- AES Encryption (Modern ZIP Encryption)
    - Mã hóa mạnh
    - không có lỗ hổng plain text attacks


