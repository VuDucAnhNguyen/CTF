## Linux commands
strings, cat, grep, find

## Exiftool
Sử dụng exiftool để xem metadata từ file
```
exiftool [file_name]
```

## Binwalk
Sử dụng binwalk để tính entropy
```
binwalk -E [file_name]
```
Sử dụng binwalk để trích xuất file ẩn. binwalk quét và phát hiện các file ẩn và gọi đến các công cụ có sẵn trong OS để trích xuất
```
binwalk -e [file_name]
```
>[!Note] 
> Trong trường hợp hệ điều hành không có sẵn công cụ trích xuất, có thể sử dụng dd (Data Duplicator) để trích xuất raw data.
```
dd if=[input_file] of=[output_file] bs=[block_size] skip=[start_block] count=[num_block]
```
