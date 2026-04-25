## Lý thuyết
### Registry key hệ thống
Đây là các file chứa cấu hình cho toàn bộ máy tính (phần cứng, phần mềm đã cài, thiết lập hệ thống). Các file này nằm trong thư mục `C:\Windows\System32\config\`, trong đó có các file sau:

| REGISTRY_KEY | Ý nghĩa |
| ------------ | -------- |
| SYSTEM | Chứa cấu hình phần cứng và các Driver |
| SOFTWARE | Chứa thiết lập của các phần mềm đã cài đặt trên máy |
| SAM | (Security Accounts Manager) Chứa thông tin tài khoản và mật khẩu (dạng hash) của người dùng cục bộ |
| SECURITY | Chứa các chính sách bảo mật hệ thống |
| DEFAULT | Cấu hình mặc định cho người dùng mới |

Cơ chế DPAPI (Data Protection API) của Windows:
- Nhiều ứng dụng không quản lý khóa mã hóa mà để Windows sinh ra khóa mã hóa từ mật khẩu user => Có thể mở khóa ứng dụng bằng cách lấy khóa người dùng thông qua SAM và SYSTEM

### Registry key người dùng
Người dùng trên máy sẽ có thiết lập riêng (hình nền, icon, lịch sử file...). Dữ liệu này nằm ngay trong file `C:\Users\<Tên_User>\NTUSER.DAT`

## Các phương pháp và công cụ điều tra registry key
### Sử dụng các tool để lấy mật khẩu người dùng
Link: [mimikatz & hashcat](https://www.nitttrchd.ac.in/imee/Labmanuals/Password%20Cracking%20of%20Windows%20Operating%20System.pdf)

Trên kali linux có thể sử dụng công cụ `impacket-secretsdump` để thay thế mimikatz
```
impacket-secretsdump -sam [SAM_file] -system [SYSTEM_file] local
```
tham số `local` để thông báo phân tích ngoại tuyến. Sau khi chạy sẽ in ra theo cú pháp `USER:1000:ccf9155e3e7db453aad3b435b51404ee:3dbde697d71690a769204beb12283678:::`

| Thành phần | Ý nghĩa |
| ---------- | ---- |
| `USER` | username |
| `1000` | RID (Relative Identifier) - Mã số định danh của user trong Windows (1000 thường là user đầu tiên được tạo) |
| `ccf9155e3e7db453aad3b435b51404ee` | LM Hash - đây là mã băm theo chuẩn băm cũ (rất yếu) |
| `3dbde697d71690a769204beb12283678` | NTLM Hash - đây là mã băm thực tế Windows đang dùng |

### Một số tool khác:
- FTKImager
- RegistryExplorer
