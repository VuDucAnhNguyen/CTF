## Lý thuyết
Domain Controller (DC) là máy chủ trung tâm trong hệ thống mạng Windows Server, chịu trách nhiệm lưu trữ cơ sở dữ liệu thư mục (Active Directory) và quản lý việc xác thực (Authentication), phân quyền (Authorization) cho toàn bộ người dùng, máy trạm và tài nguyên trong một Domain.

### Các thành phần cốt lõi của Domain Controller
- Active Directory Database (NTDS.dit): Cơ sở dữ liệu lưu trữ toàn bộ thông tin về các đối tượng (Objects) như Users, Groups, Computers, Printers và Policy.

- Kerberos Key Distribution Center (KDC): Dịch vụ cấp phát vé xác thực (Ticket-Granting Service & Authentication Service), là phương thức xác thực mặc định và an toàn nhất trên Windows AD. [Note](../../Network/Kerberos.md)

- NTLM Authentication: Giao thức xác thực cũ hơn, được sử dụng cho mục đích tương thích ngược. [Note](../../Network/NTLM.md)

- DNS Server: Định vị máy chủ DC và các dịch vụ mạng (thông qua các bản ghi SRV như _kerberos, _ldap).

- Group Policy Engine: Áp đặt các chính sách bảo mật, cấu hình phần mềm và hạn chế quyền hạn đồng loạt xuống các máy trạm (GPO).

- SYSVOL Folder: Thư mục chia sẻ lưu trữ các kịch bản đăng nhập (scripts) và chính sách Group Policy để đồng bộ giữa các DC.

### Thành phần phụ trợ / Legacy (Tùy chọn)
- WINS Server: Dịch vụ phân giải tên NetBIOS thành địa chỉ IP qua nhiều subnet (routed network), chủ yếu phục vụ các hệ thống hoặc ứng dụng Windows đời cũ. [Note](./WINS_Server.md)

