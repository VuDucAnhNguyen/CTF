## Các phương pháp và công cụ điều tra bộ nhớ RAM
### strings + grep
Để đọc những chuỗi trong RAM:
- Đối với một số ứng dụng, web,.. dữ liệu được lưu dưới dạng  UTF-8, ASCII nên có thể dùng `strings`
- Đối với Cấu trúc Kernel & OS Internals, file thực thi PE metadata, biến môi trường thì được lưu dưới dạng Little-Endian 16-bit nên cần dùng `strings -el`

### Voltality 3
Đây là những kỹ thuật cơ bản và phổ biến nhất, sử dụng các plugin được tích hợp sẵn trong Volatility Framework để tự động trích xuất thông tin có cấu trúc.

```
vol -f [file_name] [plugin]
```
Một số plugin hay dùng:
| Nhóm | Plugin | Chức năng |
| - | - | - |
|Overall Information | windows.info | Lấy thông tin tổng quan về file dump (OS, kiến trúc CPU, thời gian dump) |
| Process Analyst | windows.pslist | Liệt kê các tiến trình đang chạy bằng cách duyệt quay Doubly-Linked List của Kernel (ActiveProcessLinks) |
| | windows.pstree | Hiển thị các tiến trình dưới dạng cây (Cha - Con).Hiển thị các tiến trình dưới dạng cây (Cha - Con)|
| | windows.psscan | Tìm các tiến trình mới bị tắt hoặc bị ẩn đi |
| Artifact Extraction | windows.cmdline | Hiển thị câu lệnh và các tham số truyền vào khi tiến trình đó được khởi chạy |
| | windows.filescan | Tìm các file đã được nạp hoặc cache trong RAM và trả về offset|
| | windows.dumpfiles | Dump file từ RAM ra ổ cứng dựa vào offset:  `vol -f [file_name] windows.dumpfiles --virtaddr [offset]` |
| | windows.memmap | Dump toàn bộ không gian bộ nhớ của 1 tiến trình (bao gồm cả heap, stack, các thư viện đính kèm): `vol -f [file_name] -o [output_dir] windows.memmap --dump --pid [PID]` |
| Network & Configuration | windows.netscan | Liệt kê các kết nối (TCP/UDP), port đang mở và IP nguồn, đích |
| | windows.envars | Hiển thị các biến môi trường của các tiến trình: `vol -f [file_name] windows.envars --pid [PID]` |
| | windows.registry.printkey | Hiển thị nội dung của các Key hoặc Value bên trong Windows Registry: `vol -f [file_name] windows.registry.printkey --string "keyword_to_find"` |

VD: [Green Goblin](../../Writeups/V1T_2026/Forensics/Green_Goblin/writeup.md)