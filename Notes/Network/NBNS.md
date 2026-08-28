## Lý thuyết
NBNS (NetBIOS Name Service) là giao thức định tuyến và ánh xạ tên NetBIOS của thiết bị sang địa chỉ IPv4 tương ứng (hoạt động tại tầng Application, sử dụng cổng UDP 137).

NBNS hoạt động theo 2 cơ chế chính:
- Point-to-Point: Máy tính gửi trực tiếp bản tin Unicast đến WINS Server để đăng ký/làm mới tên (Name Refresh) hoặc hỏi địa chỉ IP của máy khác.
- Broadcast: Nếu k tìm thấy WINS Server, máy sẽ gửi tin broadcast mạng LAN dể xác định máy có tên NetBIOS cần tìm

## Các kỹ thuật tấn công NBNS & WINS Server
### NBNS Spoofing 
- Gói tin NBNS có thể bị giả mạo do không có xác thực hay chữ ký mã hóa
- Gói tin truy vấn dạng Broadcast (Name Query): Kẻ tấn công chỉ cần lắng nghe gói tin broadcast hỏi tên trên mạng LAN rồi lập tức trả lời nhận mình chính là máy đó (Name Query Response kèm IP của Attacker)