## Lý thuyết
NTLM (NT LAN Manager) là một bộ giao thức xác thực bảo mật kế thừa (legacy) của Microsoft, hoạt động dựa trên cơ chế thách thức - phản hồi (Challenge-Response) bằng việc sử dụng hàm băm mật khẩu (NT hash).

### Cơ chế hoạt động:

Trường hợp 1: Xác thực Standalone / Local (Client $\leftrightarrow$ Server)

1. Negotiate: Client gửi gói tin khởi tạo kết nối, thông báo các tính năng bảo mật được hỗ trợ.

2. Challenge: Server tạo ra một chuỗi ngẫu nhiên (Server Challenge / Nonce) và gửi lại cho Client.

3. Authenticate:

    - Client lấy NT hash của mật khẩu (sinh từ MD4(UTF-16LE(password))), kết hợp cùng Server Challenge + Client Challenge + Timestamp để tính ra giá trị phản hồi NTLMv2 Response.

    - Client gửi Response kèm Username và Domain lên Server.

    - Server lấy NT hash của user (lưu trong file SAM cục bộ), thực hiện cùng phép tính toán học. Nếu kết quả trùng khớp với Response nhận được $\rightarrow$ Cho phép đăng nhập.

Trường hợp 2: Xác thực trong Active Directory Domain (Pass-Through Authentication)

Khi Client truy cập một Server thành viên trong Domain:

- Các bước 1, 2, 3 diễn ra tương tự giữa Client và Server.

- Ở bước 3, do Server thành viên không lưu mật khẩu của Domain User, Server sẽ đóng gói chuỗi Challenge và NTLM Response gửi lên Domain Controller (DC) qua giao thức Netlogon (gọi là Pass-Through Authentication).

- DC kiểm tra với cơ sở dữ liệu ntds.dit và trả kết quả thành công/thất bại về cho Server.

## Các kỹ thuật tấn công NTLM
### NTLM Relay Attack
- Kẻ tấn công đứng giữa chặn bắt gói tin xác thực  từ máy nạn nhân và chuyển tiếp (relay) nguyên vẹn sang một máy chủ dịch vụ khác (như SMB, HTTP, LDAP, AD CS).

### NetNTLM Hash Cracking
- Đánh cắp gói tin Authentication (NetNTLMv1 / NetNTLMv2 hash), sau đó đưa vào máy offline dùng Hashcat để bẻ khóa từ điển/brute-force.