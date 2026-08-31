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

1. `KRB_AS_REQ`: Client gửi yêu cầu kèm timestamp được mã hóa bằng password hash của domain user (Pre-Authentication).

2. `KRB_AS_REP`: KDC giải mã timestamp để xác thực mật khẩu. KDC trả về:

    - TGT (Ticket Granting Ticket): Được mã hóa bằng secret key của tài khoản krbtgt.

    - Logon Session Key: Mã hóa bằng password hash của client.

Pha 2: Lấy vé dịch vụ (Ticket-Granting Service Exchange)

3. `KRB_TGS_REQ`: Client gửi TGT + Authenticator (mã hóa bằng Logon Session Key) + tên SPN (Service Principal Name) muốn truy cập.

4. `KRB_TGS_REP`: KDC giải mã TGT bằng krbtgt key, xác thực authenticator, rồi trả về:

    - TGS Ticket (Service Ticket): Được mã hóa bằng password hash của tài khoản chạy dịch vụ đó.

    - Service Session Key: Mã hóa bằng Logon Session Key.

Pha 3: Xác thực với Dịch vụ (Client/Server Exchange)

5. `KRB_AP_REQ`: Client gửi Service Ticket + Authenticator mới (mã hóa bằng Service Session Key) đến máy chủ dịch vụ.

6. `KRB_AP_REP` (Tùy chọn): Server giải mã ticket bằng key của chính nó, xác nhận client, và có thể phản hồi lại để thực hiện xác thực hai chiều (Mutual Authentication).

## Các kỹ thuật tấn công Kerberos
### Kerberoasting
Từ một tài khoản Domain User bất kỳ bị chiếm quyền, kẻ tấn công truy vấn Active Directory để liệt kê các tài khoản dịch vụ có gán SPN. Kẻ tấn công sau đó gửi yêu cầu `TGS-REQ` lên KDC để xin vé dịch vụ. Gói tin `TGS-REP` trả về chứa vé dịch vụ có phần dữ liệu được mã hóa bằng hash mật khẩu của tài khoản dịch vụ đó. Kẻ tấn công trích xuất bản mã này và thực hiện offline cracking.

>[!Note] 
> SPN (Service Principal Name) là một định danh duy nhất dùng để liên kết một dịch vụ mạng với một tài khoản chịu trách nhiệm chạy dịch vụ đó.

[>!Note]

###  AsREP roasting
Kẻ tấn công xác định các tài khoản người dùng đã bị tắt tính năng Kerberos Pre-Authentication (`DONT_REQ_PREAUTH`). Sau đó, kẻ tấn công mạo danh các tài khoản này để gửi trực tiếp yêu cầu `AS-REQ` lên KDC (không cần quyền đăng nhập trước). KDC bỏ qua bước xác thực trước và trả về gói tin `AS-REP`, trong đó phần dữ liệu phản hồi được mã hóa bằng khóa dẫn xuất từ mật khẩu của tài khoản mục tiêu. Kẻ tấn công lưu lại phần mã hóa này để thực hiện offline cracking.

