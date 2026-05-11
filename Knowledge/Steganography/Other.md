## Các phương pháp và công cụ ẩn tin
### Ẩn tin vào .ELF bằng steg86
steg86 chủ yếu khai thác các đặc điểm của tập lệnh x86 để giấu tin

#### Cài đặt steg86
Cài đặt cargo và steg86
```
sudo apt update && sudo apt install cargo -y
cargo install steg86
```
<br>

Thêm dòng này vào cuối file `~/.zshrc` để chạy trực tiếp trong terminal
```
export PATH="$HOME/.cargo/bin:$PATH"
``` 
<br>
Chạy `source ~/.zshrc` để áp dụng ngay lập tức

#### Sử dụng
Embedding:
```
steg86 embed [file_name] <<< "here is my secret message"
```
<br>

Extraction:
```
steg86 extract [file_name]
```

VD: [Stegmaxxing](../../Writeups/BKISC_CTF_2026/Miscellaneous/Stegmaxxing/writeup.md)

