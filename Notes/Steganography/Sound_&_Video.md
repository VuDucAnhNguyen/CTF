## Lý thuyết


## Các phương pháp và công cụ ẩn tin trong âm thanh
### Sử dụng minimodem
Minimodem là công cụ có thể biến văn bản thành âm thanh và ngược lại nhờ sử dụng kỹ thuật FSK (Frequency Shift Keying) thay đổi tần số để biểu diễn ký hiệu

VD: [Wiretap](../../Writeups/CIT_2026/Forensics/Wiretap/writeup.md)

```
minimodem [mode] -f [file_name] [Baud_rate]
```

| mode hay dùng | ý nghĩa |
| --- | ------- |
| --rx | recieve, chế độ nhận để chuyển file âm thanh thành văn bản |
| --tx | transmit, chế độ phát để chuyển văn bản thành âm thanh |
| -a | auto-carrier, tự động xác định tần số mark (bit 1) và space (bit 0) |
| -f | file, mã hóa/ giải mã từ file |
| -M [mark] | đặt giá trị tần số mark  |
| -S [space] | đặt giá trị tần số space |

Baud rate: là tốc độ bit được truyền đi mỗi giây, baud rate của máy phát và máy thu phải bằng nhau thì mới có thể đọc dữ liệu. Các giá trị phổ biến: 300, 1200, 1400

[Đọc thêm](https://manpages.ubuntu.com/manpages/noble/man1/minimodem.1.html)

### Sử dụng Audacity
Audacity giúp quan sát dạng sóng, phân tích phổ âm (spectrogram), giúp xác định mark và space để dùng cho minimodem,..

VD: [Dog barking](../../Writeups/CIT_2026/Miscellaneous/Dog_barking/writeup.md)

### Phone call
Phần bắt đầu của cuộc điện thoại là DTMF (Dual-Tone Multi-Frequency - Âm kép đa tần) là hệ thống tín hiệu viễn thông để mã hóa các phím bấm (0-9, *, #). Sử dụng multimon-ng để lấy số điện thoại (cần đưa sample rate về 22050Hz để sử dụng multimon-ng)
```
sox [file_name] -r 22050  [output_name]
multimon-ng -c -a DTMF -t [output_type] [output_name]
```
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

### Kỹ thuật channel subtraction
Đối với âm thanh định dạng stereo, file âm thanh gồm 2 track chồng lên nhau là left và right để tái tạo âm thanh nhằm tạo hiệu ứng âm thanh trong không gian. Kỹ thuật channel subtraction bằng cách lấy 1 kênh trừ đi kênh còn lại, có thể giúp ẩn thông điệp.

VD: [Stegmaxxing](../../Writeups/BKISC_CTF_2026/Miscellaneous/Stegmaxxing/writeup.md)


### Bộ công cụ ffmpeg
#### ffprobe
Dùng để trích xuất và phân tích toàn bộ nội dung chi tiết của file âm thanh hoặc video (hide_banner để ẩn cấu hình của ffmpeg)
```
ffprobe -hide_banner [file_name]
```
#### ffmpeg
Có thể sử dụng để trích xuất, chỉnh sửa các file âm thanh, video
```
# lệnh trích xuất file
ffmpeg -i [file_name] -map [stream_name] -c:a copy "output_name"
```

VD: [nesting](../../Writeups/TJCTF_2026/Forensics/nesting/writeup.md)
