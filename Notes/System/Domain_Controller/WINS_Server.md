## Lý thuyết
WINS Server (Windows Internet Name Service) là máy chủ phân giải tên NetBIOS tập trung do Microsoft phát triển 
trong thời kỳ đầu trong hệ thống mạng Windows

### Cơ chế hoạt động theo unicast:
- Đăng ký tên (Registration): Khi một máy client khởi động hoặc nhận IP, nó gửi gói tin Unicast đến WINS Server chứa tên NetBIOS và địa chỉ IP của mình. WINS Server lưu thông tin này vào cơ sở dữ liệu động.
- Duy trì tên (Refresh/Keep-alive): Định kỳ (theo TTL), client gửi yêu cầu gia hạn đăng ký để xác nhận tên vẫn đang hoạt động.
- Giải phóng tên (Release): Khi tắt máy đúng quy trình, client gửi thông báo giải phóng tên để WINS Server xóa hoặc đánh dấu không còn sử dụng.
- Phân giải tên (Resolution):
    - Khi Máy A muốn kết nối tới Máy B, Máy A gửi truy vấn Unicast trực tiếp đến WINS Server hỏi IP của FILESERVER.

    - WINS Server tra cứu bảng cơ sở dữ liệu và trả về IP của Máy B.

    - Máy A thiết lập kết nối TCP/IP tới Máy B mà không cần gửi broadcast toàn mạng.
