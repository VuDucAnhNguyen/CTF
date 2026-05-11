## Ẩn tin trong các công cụ Office
### Macro VBA attack
Tấn công bằng Macro VBA là kỹ thuật tin tặc nhúng mã độc vào tệp Office (.docm, .xlsm), tự động thực thi khi người dùng bật Macro để tải xuống phần mềm độc hại, đánh cắp dữ liệu hoặc mã hóa tệp tin

Sử dụng olevba để phát hiện và trích xuất VBA macro
```
olevba [file_name]
```

### Công cụ pdf-parser và pdfimages cho file PDF
#### pdf-parser
pdf-parser là công cụ phân tích cấu trúc file PDF. Nó không dùng để đọc nội dung văn bản mà để kiểm tra các "Object" bên trong PDF

Hiển thị thống kê tổng quan về các loại object có trong file.
``` 
pdf-parser -a [file_name]
```
<br>

Xem nội dung object
```
pdf-parser -o [object_number] [file_name]
```

#### pdfimages
pdfimages là công cụ giúp trích xuất toàn bộ ảnh từ file PDF ra thành các file ảnh riêng biệt

rích xuất tất cả ảnh sang định dạng phù hợp (-all)
```
pdfimages -all [file_name] [des_path]
```