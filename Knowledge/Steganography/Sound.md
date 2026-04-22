## Lý thuyết

## Các phương pháp và công cụ ẩn tin trong âm thanh
### Sử dụng minimodem
Minimodem là công cụ có thể biến văn bản thành âm thanh và ngược lại nhờ sử dụng kỹ thuật FSK (Frequency Shift Keying) thay đổi tần số để biểu diễn ký hiệu

VD: https://github.com/VuDucAnhNguyen/CTF/blob/main/Writeups/CIT_2026/Forensics/Wiretap/writeup.md

```
minimodem [mode] -f [file_name] [Baud_rate]
```
| mode hay dùng | ý nghĩa |
| --- | ------- |
| --rx | recieve, chế độ nhận để chuyển file âm thanh thành văn bản |
| --tx | transmit, chế độ phát để chuyển văn bản thành âm thanh |
| -a | auto-carrier, tự động xác định tần số mark (bit 1) và space (bit 0) |
| -f | file, mã hóa/ giải mã từ file |

Baud rate: là tốc độ bit được truyền đi mỗi giây, baud rate của máy phát và máy thu phải bằng nhau thì mới có thể đọc dữ liệu. Các giá trị phổ biến: 300, 1200, 1400

[Đọc thêm](https://manpages.ubuntu.com/manpages/noble/man1/minimodem.1.html)

### Sử dụng Audacity
