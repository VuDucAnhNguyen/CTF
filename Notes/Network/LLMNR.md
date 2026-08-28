## Lý thuyết
LLMNR (Link-Local Multicast Name Resolution) là giao thức phân giải tên miền cục bộ, cho phép các máy tính trong cùng một mạng LAN (cùng subnet) tìm thấy địa chỉ IP của nhau mà không cần cấu hình máy chủ DNS chuyên dụng.

Sử dụng cổng UDP 5355 (định dạng gói tin tương thích với chuẩn DNS).

Gửi qua địa chỉ Multicast: 224.0.0.252 (IPv4) hoặc FF02:0:0:0:0:0:1:3 (IPv6).

### Cơ chế hoạt động trong Windows (Thứ tự phân giải tên miền)

1. DNS:

    - Windows kiểm tra file hosts và bộ nhớ cache DNS cục bộ. Nếu không có, Client gửi truy vấn Unicast tới DNS Server của hệ thống.

2. LLMNR Fallback:

    - Nếu DNS trả về Name Error (NXDOMAIN) hoặc máy chủ DNS sập, Windows tự động hạ cấp xuống LLMNR. Client gửi một gói tin Multicast UDP 5355 tới toàn bộ subnet để tìm địa chỉ máy chủ.
    - Máy chủ nhận được multicast sẽ gửi phản hồi Unicast chứa địa chỉ IP của nó về cho Client.

3. NBNS Fallback: 
    - Nếu LLMNR vẫn không có phản hồi, máy trạm tiếp tục broadcast gói NBNS.

## Các kỹ thuật tấn công LLMNR
### LLMNR Poisoning (Spoofing Attack)
- LLMNR hoàn toàn không có cơ chế xác thực hay chữ ký điện tử. Mọi thiết bị nhận được gói multicast đều có quyền trả lời và tự nhận mình là máy chủ được tìm kiếm. Từ đó có thể thực hiện thu thập hash NTLM hoặc tấn công NTLM relay