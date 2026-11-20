# Lý thuyết
- LBA (Logical Block Addressing): Là các sector được đánh số thứ tự (LBA 0, LBA 1, LBA 2...)

## MBR (Master Boot Record)
MBR là chuẩn cũ. Bảng phân vùng nằm tại LBA 0:
- Bootstrap Code (446 bytes): Đoạn mã khởi động nhỏ để nạp hệ điều hành từ phân vùng khởi động.
- Partition Table (64 bytes): Bảng mô tả tối đa 4 phân vùng chính (Primary Partitions). Mỗi entry chiếm 16 bytes chứa thông tin về loại phân vùng, sector bắt đầu và sector kết thúc.
- Boot Signature (2 bytes): Chữ ký kết thúc mang giá trị cố định 0xAA55.

## GPT (GUID Partition Table)
```
GUID Partition Table Scheme

         +---------------------------------------+
LBA 0    |            Protective MBR             |
         +---------------------------------------+
LBA 1    |          Primary GPT Header           |  ^
         +---------+---------+---------+---------+  |
LBA 2    | Entry 1 | Entry 2 | Entry 3 | Entry 4 |  |
         +---------+---------+---------+---------+  | Primary GPT
         |                                       |  |
         |             Entries 5–128             |  |
LBA 33   |                                       |  v
         +---------------------------------------+
LBA 34   |                                       |  ^
         |              Partition 1              |  |
         |                                       |  |
         +---------------------------------------+  |
         |                                       |  |
         |              Partition 2              |  | Data
         |                                       |  |
         +---------------------------------------+  |
         |                                       |  |
         |         Remaining Partitions          |  |
LBA -34  |                                       |  v
         +---------+---------+---------+---------+
LBA -33  | Entry 1 | Entry 2 | Entry 3 | Entry 4 |  ^
         +---------+---------+---------+---------+  |
         |                                       |  |
         |             Entries 5–128             |  | Secondary GPT
LBA -2   |                                       |  |
         +---------------------------------------+  |
LBA -1   |         Secondary GPT Header          |  v
         +---------------------------------------+
```
### LBA 0 (Protective MBR) 
Bảng MBR giả để bảo vệ ổ đĩa, ngăn các công cụ quản lý đĩa cũ (chỉ đọc MBR) nhận nhầm ổ đĩa và ghi đè dữ liệu.
### LBA 1 (Primary GPT Header)
| Offset | Length | Contents |
| --- | --- | --- |
| `0x00` | 8 bytes | **Signature** ("EFI PART": `0x4546492050415254`) – chuỗi nhận dạng, dùng để xác nhận đây là vùng GPT header. |
| `0x08` | 4 bytes | **Revision** (GPT 1.0 có giá trị `0x00000100`) – số hiệu phiên bản chuẩn của GPT header. |
| `0x0C` | 4 bytes | **Header size** (thường là `0x5C000000` hay 92 bytes, little endian) – kích thước thực tế của GPT header (tính bằng byte). |
| `0x10` | 4 bytes | **Header CRC32** (CRC32/zlib tính từ `0x00` đến hết header size, little endian) – mã kiểm tra toàn vẹn của GPT header (trường này phải đặt về `0` khi tính). |
| `0x14` | 4 bytes | **Reserved** (bắt buộc toàn số `0`) – vùng dự trữ để mở rộng chuẩn UEFI trong tương lai và căn chỉnh (padding) các trường phía sau về bội số 8-byte. |
| `0x18` | 8 bytes | **Current LBA** – địa chỉ sector (LBA) chứa chính GPT header này. |
| `0x20` | 8 bytes | **Backup LBA** – địa chỉ sector của bản sao GPT header dự phòng. |
| `0x28` | 8 bytes | **First usable LBA** – sector đầu tiên có thể dùng để tạo partition (nằm ngay sau bảng partition entries chính). |
| `0x30` | 8 bytes | **Last usable LBA** – sector cuối cùng có thể dùng để tạo partition (nằm ngay trước bảng partition entries dự phòng). |
| `0x38` | 16 bytes | **Disk GUID** (định dạng mixed endian, hay UUID trên UNIX) – mã định danh duy nhất toàn cầu của ổ đĩa vật lý. |
| `0x48` | 8 bytes | **Starting LBA of partition entries** – sector bắt đầu của mảng danh sách các partition. |
| `0x50` | 4 bytes | **Number of partition entries** – tổng số lượng entry tối đa mà mảng partition có thể chứa (thường là `128`). |
| `0x54` | 4 bytes | **Size of a single partition entry** – kích thước của mỗi partition entry (thường là `0x80` hay 128 bytes). |
| `0x58` | 4 bytes | **Partition entries CRC32** (CRC32/zlib, little endian) – mã kiểm tra toàn vẹn cho toàn bộ mảng partition entries. |
| `0x5C` | * | **Reserved** (bắt buộc toàn số `0`) – vùng dự trữ để lấp đầy phần không gian trống còn lại của sector chứa header và dành cho các mở rộng cấu trúc header sau này. |

### LBA 2 đến LBA 33 (Partition Entries)
| Offset | Length | Contents |
| --- | --- | --- |
| `0x00` | 16 bytes | **Partition type GUID** (mixed endian) – mã định danh loại phân vùng (ví dụ: EFI System, Basic Data, Linux Filesystem...), giúp hệ điều hành biết mục đích sử dụng của phân vùng này. |
| `0x10` | 16 bytes | **Unique partition GUID** (mixed endian) – mã định danh duy nhất của riêng phân vùng này (mỗi phân vùng được tạo ra sẽ có một GUID ngẫu nhiên khác nhau để phân biệt). |
| `0x20` | 8 bytes | **First LBA** (little endian) – địa chỉ sector (LBA) bắt đầu của phân vùng trên ổ đĩa. |
| `0x28` | 8 bytes | **Last LBA** (little endian, tính bao gồm cả sector này, thường là số lẻ) – địa chỉ sector (LBA) kết thúc của phân vùng trên ổ đĩa. |
| `0x30` | 8 bytes | **Attribute flags** – các cờ thuộc tính điều khiển hành vi phân vùng (ví dụ: bit 0 báo phân vùng hệ thống bắt buộc, bit 60 thiết lập chế độ chỉ đọc/read-only, bit 62 ẩn phân vùng...). |
| `0x38` | 72 bytes | **Partition name** (tối đa 36 ký tự mã hóa UTF-16LE, kết thúc bằng ký tự null) – tên nhãn hiển thị do người dùng hoặc hệ thống đặt cho phân vùng. | 

### Backup Partition Entries và Secondary GPT Header
Lưu một bản sao lưu của Partition Entries và GPT Header