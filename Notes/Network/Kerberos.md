## Lý thuyết
Kerberos là giao thức xác thực mạng dựa trên vé (ticket-based), hoạt động theo mô hình Client-Server và sử dụng bên thứ ba tin cậy (Key Distribution Center - KDC) để chứng thực danh tính mà không truyền mật khẩu qua đường truyền.

### Các thành phần cốt lõi

- Client / Principal: Người dùng hoặc dịch vụ cần xác thực.

- KDC (Key Distribution Center): Thường nằm trên Domain Controller (DC), gồm hai dịch vụ:

    - Authentication Server (AS): Xác minh danh tính người dùng ban đầu và cấp TGT.

    - Ticket Granting Server (TGS): Nhận TGT hợp lệ và cấp Ticket cho dịch vụ cụ thể (Service Ticket / TGS).

- Target Server / Service: Máy chủ chứa tài nguyên mà client muốn truy cập (file share, web, database...).

### Cơ chế hoạt động
Pha 1: Lấy vé TGT (Authentication Service Exchange)

1. KRB_AS_REQ: Client gửi yêu cầu kèm timestamp được mã hóa bằng password hash của domain user (Pre-Authentication).

2. KRB_AS_REP: KDC giải mã timestamp để xác thực mật khẩu. KDC trả về:

    - TGT (Ticket Granting Ticket): Được mã hóa bằng secret key của tài khoản krbtgt.

    - Logon Session Key: Mã hóa bằng password hash của client.

Pha 2: Lấy vé dịch vụ (Ticket-Granting Service Exchange)

3. KRB_TGS_REQ: Client gửi TGT + Authenticator (mã hóa bằng Logon Session Key) + tên SPN (Service Principal Name) muốn truy cập.

4. KRB_TGS_REP: KDC giải mã TGT bằng krbtgt key, xác thực authenticator, rồi trả về:

    - TGS Ticket (Service Ticket): Được mã hóa bằng password hash của tài khoản chạy dịch vụ đó.

    - Service Session Key: Mã hóa bằng Logon Session Key.

Pha 3: Xác thực với Dịch vụ (Client/Server Exchange)

5. KRB_AP_REQ: Client gửi Service Ticket + Authenticator mới (mã hóa bằng Service Session Key) đến máy chủ dịch vụ.

6. KRB_AP_REP (Tùy chọn): Server giải mã ticket bằng key của chính nó, xác nhận client, và có thể phản hồi lại để thực hiện xác thực hai chiều (Mutual Authentication).


