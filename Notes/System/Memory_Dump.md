## Lý thuyết
### Linux

#### 1. Cấu trúc Nhân & Mở rộng (Kernel Core & Extension)
* **Kernel Module (LKM - Loadable Kernel Module):** Tệp mã nhị phân có định dạng ELF (`.ko`) được nạp và liên kết động trực tiếp vào không gian nhân (Kernel Space - Ring 0) khi hệ thống đang vận hành mà không cần biên dịch lại mã nguồn nhân. LKM thực thi với toàn quyền trên bộ nhớ và phần cứng, thường được dùng để cài đặt trình điều khiển thiết bị (device driver) hoặc bị khai thác để triển khai rootkit nhân.
* **Kernel Object (`struct kobject`):** Cấu trúc dữ liệu trong nhân Linux dùng để quản lý vòng đời đối tượng thông qua cơ chế đếm tham chiếu (`kref`), thiết lập quan hệ phân cấp cây thư mục giữa các thành phần phần cứng/driver và đóng vai trò là cấu trúc nền tảng đại diện cho các thực thể xuất hiện trong `sysfs`.
* **sysfs (`/sys`):** Hệ thống tệp ảo (pseudo filesystem) được tạo trên RAM và mount tại thư mục `/sys`. `sysfs` xuất thông tin và các thuộc tính của các `kobject` từ Kernel Space ra User Space dưới dạng các thư mục và tệp văn bản, cho phép người dùng xem trạng thái và cấu hình các thông số của thiết bị, driver và module.
* **Taint Flag:** Trường bitmask số nguyên (`tainted_mask`) do kernel duy trì để ghi nhận các sự kiện làm mất tính toàn vẹn hoặc tính ổn định chuẩn của nhân hệ điều hành. Các cờ tiêu chuẩn gồm:
  * `O` (`OOT_MODULE`): Module được biên dịch ngoài cây mã nguồn chính thức của Linux kernel (Out-Of-Tree).
  * `E` (`UNSIGNED_MODULE`): Module không có chữ ký số điện tử hợp lệ hoặc cơ chế kiểm tra chữ ký bị vô hiệu hóa.
  * `P` (`PROPRIETARY`): Module sử dụng giấy phép mã nguồn đóng, không tương thích với giấy phép GPL.

---

#### 2. Giao tiếp & Trừu tượng hóa Tài nguyên (I/O & Syscall Interface)
* **File Descriptor (FD):** Chỉ số nguyên không âm đại diện cho một kênh nhập/xuất (I/O) đang mở của một tiến trình, được quản lý trong bảng mô tả tệp (`task_struct->files`). Theo quy chuẩn: FD `0` là luồng nhập chuẩn (stdin), FD `1` là luồng xuất chuẩn (stdout), FD `2` là luồng lỗi chuẩn (stderr). Khi cả ba FD này cùng trỏ tới một socket mạng TCP/IP, tiến trình đó đang vận hành theo cơ chế chuyển hướng I/O của Reverse Shell.
* **Syscall Table (`sys_call_table`):** Mảng chứa các con trỏ hàm trỏ tới địa chỉ bộ nhớ của các hàm xử lý Lời gọi hệ thống (System Call handler như `sys_read`, `sys_write`, `sys_getdents64`). Bảng này là điểm tiếp nhận và chuyển tiếp các yêu cầu dịch vụ từ User Space (Ring 3) vào Kernel Space (Ring 0).

---

#### 3. Kỹ thuật Can thiệp & Giám sát Hệ thống (Hooking & Tracing Mechanisms)
* **Hook (Hooking):** Kỹ thuật chặn bắt luồng thực thi lệnh hoặc lời gọi hàm để chuyển hướng xử lý sang một đoạn mã khác trước khi (hoặc thay vì) thực thi hàm gốc. Kỹ thuật này được dùng để thay đổi tham số đầu vào, biến đổi dữ liệu trả về hoặc ngăn chặn việc thực thi của hàm đích.
* **Ftrace (Function Tracer):** Framework truy vết hàm cấp nhân được hỗ trợ bởi cờ biên dịch `-pg`, chèn sẵn các điểm neo thực thi (`nop` hoặc `__fentry__`) tại phần mở đầu (prologue) của các hàm kernel. Bằng cách đăng ký cấu trúc `ftrace_ops` kèm cờ `IPMODIFY`, module có thể can thiệp vào thanh ghi con trỏ lệnh (`regs->ip`) để chuyển hướng luồng thực thi sang hàm thay thế mà không cần chỉnh sửa trực tiếp bảng `sys_call_table`.
* **Tracepoint:** Điểm thăm dò tĩnh (static probe) được đặt cố định trong mã nguồn kernel bằng macro. Khi được kích hoạt, tracepoint cho phép đăng ký hàm thăm dò (probe function/callback) để đọc các biến và tham số nội bộ tại thời điểm thực thi mà không làm thay đổi luồng điều khiển của hàm gốc.
* **Centralized Callback Function:** Hàm xử lý sự kiện tập trung (dispatcher/callback) được đăng ký với framework truy vết (như Ftrace) để tiếp nhận toàn bộ các lời gọi hàm bị can thiệp. Thay vì gán từng hàm bị hook với một hàm độc lập, hệ thống chuyển toàn bộ luồng thực thi về hàm này; tại đây, con trỏ lệnh gốc (`ip`) được kiểm tra để xác định danh tính hàm đang gọi, thực hiện lưu trữ trạng thái thanh ghi CPU và chuyển tiếp luồng thực thi tới hàm thay thế tương ứng.

## Các phương pháp và công cụ điều tra bộ nhớ RAM
### strings + grep
Để đọc những chuỗi trong RAM:
- Đối với một số ứng dụng, web,.. dữ liệu được lưu dưới dạng  UTF-8, ASCII nên có thể dùng `strings`
- Đối với Cấu trúc Kernel & OS Internals, file thực thi PE metadata, biến môi trường thì được lưu dưới dạng Little-Endian 16-bit nên cần dùng `strings -el`

### Volatality 3
Đây là những kỹ thuật cơ bản và phổ biến nhất, sử dụng các plugin được tích hợp sẵn trong Volatility Framework để tự động trích xuất thông tin có cấu trúc.

```
vol -f [file_name] [plugin]
```

Symbol Table (bảng biểu tượng) là thành phần cốt lõi giúp công cụ hiểu được cấu trúc dữ liệu nhị phân bên trong một bản dump RAM (tên cấu trúc dữ liệu, kích thước, độ lệch dữ liệu). Symbol Table cung cấp toàn bộ bản đồ giải mã này dưới định dạng ISF (Intermediate Symbol Format) — bản chất là các file JSON (hoặc nén .json.xz). Để nạp symbol table thì cần nạp vào `volatility3/framework/symbols/`

#### Windows

Một số plugin hay dùng:

| Nhóm | Plugin | Chức năng |
| :--- | :--- | :--- |
| **Overall Information** | `windows.info` | Lấy thông tin tổng quan file dump (OS, build, kiến trúc CPU, thời gian chụp RAM). |
| **Process Analysis** | `windows.pslist` | Liệt kê các tiến trình đang chạy bằng cách duyệt danh sách liên kết kép (`ActiveProcessLinks`). |
| | `windows.pstree` | Hiển thị quan hệ phân cấp cha - con (`PPID - PID`) giữa các tiến trình dạng cây thư mục. |
| | `windows.psscan` | Quét toàn bộ pool tag bộ nhớ để tìm tiến trình đã thoát hoặc bị rootkit ẩn bằng DKOM. |
| **Artifact Extraction** | `windows.cmdline` | Trích xuất dòng lệnh thực thi đầy đủ kèm tham số truyền vào khi tiến trình khởi chạy. |
| | `windows.filescan` | Quét con trỏ file trong bộ nhớ cache/RAM và trả về địa chỉ offset (`virtaddr`). |
| | `windows.dumpfiles` | Trích xuất file từ RAM ra ổ đĩa: `vol -f [file] windows.dumpfiles --virtaddr [offset]`. |
| | `windows.memmap` | Dump toàn bộ không gian bộ nhớ của tiến trình: `vol -f [file] -o [dir] windows.memmap --dump --pid [PID]`. |
| **Network & System State** | `windows.netscan` | Liệt kê các kết nối mạng (TCP/UDP), cổng lắng nghe, trạng thái, IP và PID sở hữu. |
| | `windows.envars` | Trích xuất biến môi trường của tiến trình: `vol -f [file] windows.envars --pid [PID]`. |
| | `windows.registry.printkey` | Đọc nội dung Registry Key/Value: `vol -f [file] windows.registry.printkey --string "key_name"`. |
| **Kernel & Rootkit Integrity** | `windows.ssdt` | Kiểm tra bảng System Service Descriptor Table (`SSDT`) để phát hiện SSDT hooking. |
| | `windows.driverscan` | Quét các driver kernel (`.sys`) đã nạp vào RAM, phát hiện driver không chính chủ/độc hại. |
| | `windows.malfind` | Quét các trang bộ nhớ có quyền thực thi bất thường (`PAGE_EXECUTE_READWRITE`) để phát hiện DLL Injection, Shellcode. |

VD: [Green Goblin](../../Writeups/V1T_2026/Forensics/Green_Goblin/writeup.md)

---

#### Linux

Một số plugin hay dùng:

| Nhóm | Plugin | Chức năng |
| :--- | :--- | :--- |
| **Overall Information** | `linux.banner` | Trích xuất chuỗi Linux banner (kernel version, compiler) để chọn đúng Symbol Table. |
| **Process Analysis** | `linux.pslist` | Liệt kê các tiến trình đang chạy bằng cách duyệt danh sách liên kết `tasks` trong `task_struct`. |
| | `linux.pstree` | Hiển thị quan hệ cha - con (`parent-child`) giữa các tiến trình dưới dạng cây. |
| | `linux.psscan` | Quét tìm các cấu trúc `task_struct` bị DKOM ẩn đi hoặc tiến trình đã kết thúc nhưng chưa giải phóng. |
| **Artifact Extraction** | `linux.cmdline` | Trích xuất dòng lệnh thực thi và đối số từ không gian bộ nhớ của tiến trình. |
| | `linux.lsof` | Liệt kê file descriptors (FD) đang mở (file, socket mạng, pipe) để phát hiện shell redirect. |
| | `linux.proc.Maps` | Xem Virtual Memory Areas (VMA) và dump bộ nhớ tiến trình: `vol -f [file] -o [dir] linux.proc.Maps --dump --pid [PID]`. |
| **Network & System State** | `linux.sockstat` | Liệt kê các socket mạng (TCP, UDP, Unix), IP/Port, trạng thái kết nối và tiến trình sở hữu. |
| | `linux.envars` | Trích xuất biến môi trường của tiến trình: `vol -f [file] linux.envars --pid [PID]`. |
| | `linux.kmsg` | Trích xuất log bộ đệm nhân (`dmesg`), phát hiện module độc hại qua cờ vấy bẩn (**taint flags**). |
| **Kernel & Rootkit Integrity** | `linux.lsmod` | Liệt kê danh sách các Kernel Module (LKM) đã nạp để phát hiện driver lạ. |
| | `linux.tracing.ftrace.CheckFtrace` | Phát hiện rootkit can thiệp hàm bằng **Ftrace**, đếm số lượng hook và xác định hàm callback trung tâm. |
| | `linux.tracing.tracepoints.CheckTracepoints` | Quét các **Tracepoint** trong nhân (như `sched_process_fork`) bị rootkit gắn probe/handler can thiệp. |
