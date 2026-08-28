## Lý thuyết
LDAP (Lightweight Directory Access Protocol) và LDAP (Connectionless LDAP) là các giao thức chuẩn mạng dùng để truy vấn, xác thực và quản lý các đối tượng (người dùng, máy tính, nhóm quyền) trong cơ sở dữ liệu thư mục tập trung như Active Directory (AD).

### LDAP
LDAP hoạt động trên TCP (Port 389) hoặc LDAPS qua TLS/SSL (Port 636). Kết nối LDAP có hướng, thực hiện bắt tay 3 bước TCP, sau đó thực hiện quá trình liên kết (LDAP Bind) để xác thực phiên làm việc.

#### Mục đích
Thực hiện các thao tác quản trị, truy vấn sâu và chỉnh sửa cấu trúc thư mục Active Directory.

#### Cơ chế hoạt động
1. Client bắt tay TCP với DC/LDAP Server.

2. Gửi yêu cầu bindRequest (Anonymous, NTLM/GSS-API, hoặc Kerberos).

3. Server trả lời bindResponse chấp thuận.

4. Client gửi các truy vấn phức tạp (searchRequest) để đọc/ghi thuộc tính thư mục, chỉnh sửa GPO, phân quyền ACL.

5. Đóng phiên bằng unbindRequest.

### CLDAP
CLDAP hoạt động trên UDP (Port 389). Không bắt tay TCP, không cần LDAP Bind. Client gửi 1 gói tin UDP query và Server phản hồi trực tiếp 1 gói tin UDP.

#### Mục đích
Định vị máy chủ Domain Controller gần nhất (DC Locator) nhanh chóng và tiết kiệm băng thông mạng.

#### Cơ chế hoạt động
1. Client gửi một gói tin UDP đơn lẻ (searchRequest) với bộ lọc Netlogon.

2. DC nhận gói tin, lập tức đóng gói toàn bộ metadata nhận dạng vào cấu trúc NETLOGON_SAM_LOGON_RESPONSE và phản hồi lại cho Client qua UDP (searchResDone).