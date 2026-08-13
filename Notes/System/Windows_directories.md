## Lý thuyết
### AppData
Thư mục `C:\Users\<User>\AppData` (thường bị ẩn) chia làm 3 nhóm chính dựa trên phạm vi hoạt động của dữ liệu:
| Thư mục | Biến môi trường | Mục đích lưu trữ |
| - | - | - |
| Roaming | `%APPDATA%` | Cấu hình & Setting cá nhân có thể đồng bộ khi đăng nhập user trên các máy khác trong cùng Domain (Active Directory) |
| Local | `%LOCALAPPDATA%` | Dữ liệu cố định trên máy hiện tại, dữ liệu dung lượng lớn, cache, temp không mang đi máy khác được |
| LocalLow | `%USERPROFILE%\AppData\LocalLow` | Dữ liệu từ các ứng dụng chạy ở mức đặc quyền thấp (Low Integrity Level / Protected Mode) để đảm bảo an toàn sandbox |

### Thư mục dữ liệu dùng chung & Hệ thống
- `C:\ProgramData` (`%PROGRAMDATA%`):
    - Lưu trữ dữ liệu cấu hình/hoạt động của ứng dụng dùng chung cho TẤT CẢ User trên máy.
- `C:\Windows\System32` vs `C:\Windows\SysWOW64`:
    - `System32`: Chứa file DLL và binary 64-bit của hệ thống (giữ tên 32 vì lý do tương thích ngược)
    - `SysWOW64`: Chứa file DLL và binary 32-bit chạy trên môi trường Windows 64-bit (Windows on Windows 64)

### Các vị trí Cache, Temp, Dump quan trọng
| Loại dữ liệu | Đường dẫn | Chi tiết |
| - | - | - |
| User Temp | `%TEMP% hoặc %LOCALAPPDATA%\Temp`	| Tệp tạm của ứng dụng người dùng (payload, installer, log tạm) |
|System Temp | `C:\Windows\Temp` | Tệp tạm do các dịch vụ hệ thống tạo ra |
| Prefetch Cache | `C:\Windows\Prefetch` | File `.pf` ghi lại vết thực thi ứng dụng, số lần chạy và timestamp gần nhất |
| Thumbnail Cache | `%LOCALAPPDATA%\Microsoft\Windows\Explorer` | File `thumbcache_*.db` lưu ảnh xem trước, giúp khôi phục ảnh/doc đã bị xóa |
| File History | `%LOCALAPPDATA%\Microsoft\Windows\FileHistory\Data` | Bản sao lưu dữ liệu người dùng qua các mốc thời gian trong quá khứ  |
|Windows Jump Lists	|`%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations`	| Lưu danh sách tệp/thư mục được mở gần đây hoặc ghim theo từng ứng dụng <br> Chi tiết: [Jump_Lists.md](Jump_Lists.md) |
| LNK Files | `%APPDATA%\Microsoft\Windows\Recent` | Shortcut tự động tạo khi mở file; chứa đường dẫn gốc, volume serial và timestamp |

## Các phương pháp và công cụ điều tra thư mục Windows
### ChromeCacheView.exe
- Là công cụ hỗ trợ xem và trích xuất cache trình duyệt và ứng dụng sử dụng nhân Chromium

VD: VD: [L3ak_APT](../../Writeups/L3akCTF_2026/Forensics/L3ak_APT/writeup.md)

### Một số tool khác:
- FTKImager