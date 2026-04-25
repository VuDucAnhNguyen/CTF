## Các phương pháp và công cụ điều tra ứng dụng
### Sử dụng bmc-tool cho RDP cache
Link [Github](https://github.com/ANSSI-FR/bmc-tools)

bmc-tool là 1 script python giúp phân tích và trích xuất dữ liệu từ file RDP Bitmap cache ví dụ như `.bmc`, `.bin` và ánh xạ file đã được tạo trong giao thức RDP

>[!Note]
> RDP Bitmap cache là 1 tính năng của RDP có chức năng lưu trữ các mảnh nhỏ (tiles) của hình ảnh màn hình từ phiên làm việc từ xa vào ổ đĩa của máy client nhằm tăng tốc RDP nhờ chỉ cần gửi các phần thay đổi thay vì toàn bộ hình ảnh màn hình

```
python3 bmc-tool.py -s [cache_file_path] -d [output_path] -b
```
Kết quả tạo ra sẽ là thư mục output chứa các ảnh tiles `.bmp`, tham số `-b` giúp tạo ra 1 ảnh ghép tất cả các ảnh `.bmp` này lại