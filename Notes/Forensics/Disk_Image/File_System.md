# Lý thuyết
## FAT32
| Offset | Length | Contents |
| --- | --- | --- |
| Sector 0 | 1 sector | **Boot Sector (VBR)** – chứa BIOS Parameter Block (khai báo kích thước sector, cluster, số sector dự trữ R, kích thước bảng FAT F) và mã mồi khởi động hệ điều hành (nếu phân vùng có khả năng boot). |
| Sector 1 | 1 sector | **FSInfo Sector** – lưu trữ thông tin trạng thái hệ thống file (tổng số cluster trống hiện tại và vị trí cluster trống tiếp theo được gợi ý), giúp hệ điều hành cấp phát dung lượng nhanh hơn mà không cần quét lại toàn bộ bảng FAT. |
| Sector 2 – 5 | 4 sectors | **Reserved Boot Code** – vùng dự trữ dành cho phần mã khởi động mở rộng (do Boot Sector ở Sector 0 không đủ chỗ chứa hết) hoặc được điền toàn số `0` nếu không sử dụng. |
| Sector 6 | 1 sector | **Backup Boot Sector** – bản sao dự phòng nguyên vẹn của Sector 0 (và thường kèm theo bản sao của FSInfo ở Sector 7), dùng để khôi phục khi Boot Sector chính bị hỏng. |
| Sector 7 – (R - 1) | R - 7 sectors | **Reserved Padding** – vùng đệm dự trữ trống (thường điền số `0`) để căn chỉnh vị trí bắt đầu của bảng FAT vào ranh giới vật lý tối ưu của ổ đĩa. |
| Sector R | F sectors | **FAT1 (File Allocation Table 1)** – bảng cấp phát file chính, hoạt động như một danh sách liên kết để theo dõi chuỗi các cluster tạo nên một file và đánh dấu trạng thái cluster (trống, đang dùng, lỗi/bad sector hoặc kết thúc file). |
| Sector R + F | F sectors | **FAT2 (File Allocation Table 2)** – bản sao dự phòng đồng bộ của bảng FAT1, giúp bảo vệ dữ liệu và sửa lỗi nếu bảng FAT1 gặp sự cố đọc/ghi. |
| Sector R + 2F | Phần còn lại | **Data Region** (bắt đầu tính từ Cluster 2) – vùng lưu trữ nội dung dữ liệu thực tế của các file và các bảng thư mục (**Directory Entry**, cố định 32 bytes/entry chứa tên, thuộc tính, kích thước và cluster đầu tiên của file/thư mục con). |

## NTFS
| Offset | Length | Contents |
| --- | --- | --- |
| Sector 0 | 1 sector | **Partition Boot Sector (`$Boot`)** – chứa BIOS Parameter Block (84 bytes đầu khai báo kích thước sector, cluster, tổng số sector) và tọa độ Cluster bắt đầu của `$MFT` (tại byte offset `0x30`), giúp hệ điều hành định vị bảng quản lý file ngay khi mount phân vùng. |
| Sector 1 | 8192 - Sector_Size bytes | **Bootstrap Code** – vùng chứa mã mồi khởi động NTLDR/BOOTMGR để nạp hệ điều hành Windows (cùng với Sector 0 tạo thành vùng siêu dữ liệu `$Boot`). |
| Byte 8192 (Cluster 2) | Phần lớn dung lượng phân vùng | **Data Area** – vùng lưu trữ nội dung dữ liệu thực tế của các file lớn (Non-resident data) và các file quản trị hệ thống ẩn như `$Bitmap` (theo dõi cluster trống), `$LogFile` (nhật ký giao dịch), `$MFTMirr` (bản sao 4 record đầu của `$MFT`)... |
| Cluster_MFT x Cluster_Size | 1024 bytes / record | **`$MFT` (Master File Table)** – bảng cơ sở dữ liệu trung tâm quản lý toàn bộ file và thư mục trên phân vùng; mỗi MFT Record lưu trữ các thuộc tính metadata (tên, quyền, thời gian, danh sách Data Runs) và chứa trực tiếp dữ liệu nếu file có kích thước nhỏ (< ~700 bytes, gọi là Resident data). |
| Ngay sau `$MFT` | ~12.5% dung lượng phân vùng | **MFT Zone** – vùng không gian trống được hệ thống ưu tiên giữ chỗ riêng ngay liền kề sau `$MFT` để bảng này có thể tự mở rộng liên tục khi tạo thêm file mới mà không bị phân mảnh (chỉ bị trưng dụng lưu dữ liệu thường khi phân vùng gần đầy). |
| Sector cuối cùng | 1 sector | **Backup Boot Sector** – bản sao dự phòng nguyên vẹn của Sector 0, luôn nằm ở sector vật lý cuối cùng của phân vùng để khôi phục khả năng truy cập ổ đĩa nếu Boot Sector chính bị hỏng. |

### NTFS metadata files

#### `$MFT` (Master File Table):
**Cấu trúc MFT Record**: mỗi MFT record có kích thước 1024 bytes gồm MFT header ở đầu và danh sách các thuộc tính nối tiếp nhau theo mô hình Type - Length - Value. Kích thước mỗi thuộc tính không cố định.
| Offset | Length | Content |
| - | - | - |
|`0x00`|4 bytes | Signature - Chữ ký nhận diện FILE (`46 49 4c 45`) |
|`0x04`|2 bytes| USA Offset - Vị trí bắt đầu của mảng Update Sequence Array |
|`0x06`|2 bytes| USA Count - Tổng số phần tử 2-byte trong mảng USA (thường là 3 cho record 1024B) |
|`0x14`| 2 bytes | First Attribute Offset - Vị trí bắt đầu của Attribute đầu tiên |
|`0x16`|2 bytes| Record Flags - Cờ trạng thái bản ghi: `0x00` = Đã xóa/Trống, `0x01` = Đang sử dụng (Allocated), `0x02` = Thư mục (Directory) |
| giá trị của First Attribute Offset| Biến thiên | Attributes - Các thuộc tính xếp liên tiếp |
|Cuối | 4 bytes| End Marker - Giá trị `0xFFFFFFFF` đánh dấu kết thúc danh sách thuộc tính|

**Cơ chế toàn vẹn dữ liệu**
- Vấn đề: Một MFT Record dài 1024 bytes nằm trên 2 sectors vật lý (512 bytes/sector). Nếu hệ thống bị lỗi đột ngột khi mới ghi xong sector 1 mà chưa kịp ghi sector 2, bản ghi sẽ bị hỏng.
- Cơ chế bảo vệ trên RAM trước khi ghi xuống đĩa:
  - NTFS tăng giá trị USN (Update Sequence Number) lên 1 và lưu vào phần tử đầu tiên của mảng USA (`USA[0]`).
  - Lấy 2 byte dữ liệu gốc nằm ở cuối mỗi sector (tại offset `510–511` của sector 1 và `1022–1023` của sector 2) đem cất lần lượt vào `USA[1]` và `USA[2]`.
  - Ghi đè mã USN mới vào cả hai vị trí cuối sector (`510–511` và `1022–1023`).
  - Khi đọc lại từ đĩa, nếu 2 byte cuối của các sector không trùng khớp với `USA[0]`, NTFS phát hiện ngay quá trình ghi trước đó đã bị đứt gãy.
- Thao tác Fixup (Khôi phục): Khi phân tích nhị phân MFT Record, bắt buộc phải sao chép byte gốc từ USA trả về đúng vị trí cuối mỗi sector.

**Cấu trúc Attributes**
- Attribute Type (`0x00-0x03`):
    - `0x10`: `$STANDARD_INFORMATION` (timestamps, quyền hạn, cờ file).
    - `0x20`: `$ATTRIBUTE_LIST` (danh sách trỏ tới các record mở rộng khi file quá phân mảnh).
    - `0x30`: `$FILE_NAME` (tên tệp UTF-16LE, MFT record thư mục cha, timestamps).
    - `0x80`: `$DATA` (nội dung dữ liệu của tệp; có thể có nhiều `$DATA` nếu dùng Alternate Data Streams - ADS).
    - `0xA0`: `$INDEX_ALLOCATION` (chứa các bản ghi INDX danh mục con của thư mục lớn).
    - `0xB0`: `$BITMAP` (bản đồ bit quản lý trạng thái cấp phát của `$MFT` hoặc thư mục lớn).
- Total Length (`0x04-0x07`): Tổng chiều dài của thuộc tính
- Non-Resident Flag (`0x08`)— Cờ xác định nơi lưu trữ dữ liệu:
    - `0x00` (Resident): Dữ liệu nhỏ (thường < 700–800 bytes) nằm gọn trực tiếp bên trong MFT Record, không cấp phát cluster ngoài đĩa.
    - `0x01` (Non-Resident): Dữ liệu lớn bị đẩy ra lưu ở các cluster bên ngoài. Thuộc tính trong MFT chỉ lưu thông tin quản lý và trỏ tới chuỗi Runlist.

Nếu là Resident:
- `0x10-0x13`: Kích thước dữ liệu
- `0x14-0x15`: Offset trỏ tới nơi dữ liệu bắt đầu nằm bên trong MFT record.

Nếu là Non-Resident:
- `0x10-0x17` và `0x18-0x1F`: Starting VCN và Last VCN - Phạm vi cluster ảo (tính nội bộ trong file từ 0) mà MFT record này quản lý. Dùng để ráp đúng thứ tự các mảnh khi file bị phân mảnh quá nặng phải chia Runlist sang nhiều MFT record phụ.
- `0x20-0x21`: Runlist Offset - Vị trí bắt đầu chuỗi byte Runlist tính từ đầu thuộc tính
- `0x28-0x2F`: Allocated Size - Tổng dung lượng vật lý NTFS đã cấp phát trên ổ đĩa cho thuộc tính này.
- `0x30-0x37` — Real Size: Kích thước dữ liệu thật tính đến từng byte của file. Khoảng chênh lệch giữa Allocated Size và Real Size ở cluster cuối chính là File Slack (Slack Space) thường chứa dữ liệu sót trong điều tra số.
- Cấu trúc Runlist:
  - Header (1 byte): 4 bit sau chứa số byte cho trường LCN offset, 4 bit đầu chứa số bytcho trường chiều dài
  - Length
  - LCN  Offset: lưu tọa độ tương đối so với cluster bắt đầu (LCN) của runlist trước nó. Với runlist đầu tiên thì LCN offset là giá trị tuyệt đối
  - Kết thúc bằng `0x00`

#### `$Bitmap` (Cluster Allocation Bitmap - MFT Record #6):
- Cơ chế lưu trữ: Tệp hệ thống quản lý trạng thái cấp phát của toàn bộ các Cluster (LCN) trên phân vùng NTFS. Toàn bộ chuỗi bit của bản đồ được lưu bên trong thuộc tính $DATA (`0x80`) của MFT Record #6.
- Quy ước ánh xạ Bit: Cứ 1 bit đại diện cho 1 Cluster, xếp theo thứ tự từ LSB (bit 0) đến MSB (bit 7) trong mỗi byte:
  - Bit 0: Cluster đang trống
  - Bit 1: Cluster đã được cấp phát

#### `$UsnJrnl:$J` (Update Sequence Number Journal - Stream $J):
- Cơ chế lưu trữ: Ghi nhật ký tuần tự (append-only) các sự kiện thay đổi trạng thái tệp theo thời gian thực.
- Dữ liệu thu thập: Tên tệp, File Reference Number, Parent Entry Number, timestamp và Update Reasons (`FileCreate`, `FileDelete`, `DataExtend`, `Close`, v.v.).

#### Alternate Data Streams (ADS):
- Cho phép một file chứa nhiều luồng `$DATA` độc lập bên cạnh luồng mặc định (`<filename>:<stream_name>`).
- Lưu trữ Metadata hệ thống (như luồng `:Zone.Identifier` lưu thông tin Mark-of-the-Web), hash, hoặc toàn bộ payload nhị phân/script (`.exe`, `.dll`, `.vbs`).
- Kích thước file hiển thị trên Windows Explorer không đổi dù luồng phụ chứa dữ liệu; payload có thể được nạp và thực thi trực tiếp qua các tiến trình hệ thống (`wscript.exe`, `rundll32.exe`).



## Ext4
| Offset | Length | Contents |
| --- | --- | --- |
| `0x0000` | 1024 bytes | **Boot Block (Group 0 Padding)** – dùng để chứa mã khởi động (bootloader như GRUB) hoặc bỏ trống để tránh ghi đè lên các cấu trúc boot của hệ thống. |
| `0x0400` | 1024 bytes | **Primary Superblock** – cấu trúc siêu dữ liệu cốt lõi quản lý toàn bộ phân vùng (lưu kích thước block, tổng số block/inode, số lượng trống, các tính năng hỗ trợ và trạng thái mount sạch/lỗi của filesystem). |
| `0x0800` | Block_Size - 2048 bytes | **Padding** – phần không gian đệm trống dùng để lấp đầy phần còn lại của Block 0. |
| Block 1 | G blocks | **Group Descriptor Table (GDT)** – bảng mô tả tổng hợp lưu tọa độ block của Data Block Bitmap, Inode Bitmap và Inode Table cho toàn bộ các Block Group trên phân vùng (64 bytes với ext4 64-bit). |
| Block 1 + G | R blocks | **Reserved GDT Blocks** – vùng không gian dự trữ trống ngay sau GDT, dùng để cấp phát thêm các descriptor mới cho phép mở rộng dung lượng phân vùng trực tuyến (online resize) mà không làm xáo trộn vị trí dữ liệu hiện có. |
| Block 1 + G + R | 1 block | **Data Block Bitmap** – bản đồ bit theo dõi trạng thái cấp phát của từng Data Block trong riêng Group 0 (bit `0` đánh dấu block đang trống, bit `1` đánh dấu block đã được sử dụng). |
| Block 2 + G + R | 1 block | **Inode Bitmap** – bản đồ bit theo dõi trạng thái cấp phát của từng Inode trong riêng Group 0 (bit `0` đánh dấu inode chưa dùng, bit `1` đánh dấu inode đã được gán cho một file/thư mục). |
| Block 3 + G + R | I blocks | **Inode Table** – bảng lưu trữ tập trung các cấu trúc Inode của Group 0 (mặc định 256 bytes/Inode trên ext4), chứa toàn bộ metadata của file/thư mục (quyền truy cập, UID/GID, kích thước, timestamps và cây **Extents** trỏ tới các Data Block chứa dữ liệu). |
| Block 3 + G + R + I | Phần còn lại của Group 0 | **Data Blocks** – vùng lưu trữ nội dung dữ liệu thực tế của các file và danh sách **Directory Entries** (bảng ánh xạ tên file/thư mục sang số hiệu Inode tương ứng). |

Các Block Group 1, 2, 3... có cấu trúc trên lặp lại. Để tiết kiệm dung lượng, Ext4 chỉ đặt bản sao của Superblock và GDT ở đầu các Group có số thứ tự là lũy thừa của 3, 5, 7 và group 0, 1. Các Group còn lại sẽ bắt đầu ngay bằng Data Block Bitmap.