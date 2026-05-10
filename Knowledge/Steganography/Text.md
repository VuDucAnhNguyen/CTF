## Các phương pháp và công cụ ẩn tin trong text
### Sử dụng các ký tự Zerowidth chèn vào thông điệp
Các ký tự Zerowidth này được chèn xen giữa vào các ký tự thường để ẩn đi thông điệp. Có thể sử dụng công cụ  [Unicode Steganography with Zero-Width Characters](https://330k.github.io/misc_tools/unicode_steganography.html) để decode

VD: [There's no room left](../../Writeups\CIT_2026\Steganography\Theres_no_room_left\writeup.md)

### Sử dụng white space encoding
Sử dụng công cụ [poltergeist](https://github.com/Shell-Company/poltergeist) để decode

#### Cài đặt poltergeist
Cài đặt Golang và poltergeist
```
sudo apt update && sudo apt install golang-go -y
go install github.com/shell-company/poltergeist/cmd/poltergeist@latest
```
Thêm dòng này vào cuối file `~/.zshrc` để chạy trực tiếp trong terminal
```
export PATH=$PATH:$(go env GOPATH)/bin
``` 

#### Sử dụng
Encode:
```
poltergeist -encode -file [file_name]
```
Decode:
```
poltergeist -decode -file [file_name]
```

VD: [Zopslop](../../Writeups\BKISC_CTF_2026\Miscellaneous\Zopslop\writeup.md)


