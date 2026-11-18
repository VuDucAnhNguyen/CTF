# Phân tích ảnh đĩa
## Các loại ảnh đĩa
- Nhóm ảnh thô (Raw / Bit-stream Image): `.raw`, `.img`, `.dd`
  - Là bản sao chép y nguyên từng bit (1:1) từ ổ đĩa vật lý hoặc phân vùng ra file. Không có header mô tả, không nén, không mã hóa.
  - Dung lượng file bằng đúng dung lượng ổ đĩa gốc. Có thể dùng trực tiếp các công cụ cấp thấp như dd, The Sleuth Kit, hoặc mở bằng HxD để soi từng byte mà không cần giải mã vỏ bọc.

- Nhóm ảnh đĩa máy ảo: `.vmdk` (VMware), `.vhd` / `.vhdx` (Hyper-V), `.qcow2` (QEMU/KVM)

  - Sinh ra để phần mềm ảo hóa giả lập một ổ cứng.
  - Đặc điểm: Phần đầu file chứa một đoạn Header mô tả thông số phần cứng ảo (số sector, cylinder, thông tin snapshot...). Sử dụng cơ chế cấp phát động: nó bỏ qua các vùng trống toàn số 0 và dùng bảng ánh xạ nội bộ để quản lý. Không thể tính offset vật lý trực tiếp trên file .vmdk.
- Nhóm ảnh điều tra số chuyên dụng: `.e01` (EnCase) và `.ad1` (FTK Imager)
  - `.e01` (Expert Witness Format): Là ảnh sao chép vật lý 1:1, được bọc thêm lớp vỏ điều tra số: có nén dữ liệu, chia nhỏ thành nhiều mảnh (E01, E02...), và lưu kèm metadata.
  - `.ad1` (AccessData Logical Image): là ảnh logic (Logical Image), không phải ảnh vật lý. Thay vì sao chép cả ổ đĩa từ sector 0, công cụ chỉ gom nhặt một số thư mục/file cụ thể rồi đóng gói lại kèm metadata cơ bản của các file đó.

## Đơn vị lưu trữ
- Sector: Đơn vị vật lý/cơ bản nhỏ nhất mà ổ đĩa đọc hoặc ghi.
- Block: Đơn vị dữ liệu logic dùng cho thao tác đọc/ghi I/O của hệ điều hành, cơ sở dữ liệu hoặc tầng lưu trữ, có kích thước bằng hoặc là bội số của sector.
- Cluster: Nhóm gồm nhiều sector liền kề do hệ thống tệp tin quản lý; là đơn vị nhỏ nhất được cấp phát khi lưu một tệp tin.
- Partition: Phân vùng logic lớn chia một ổ đĩa vật lý thành các khu vực độc lập. mỗi khu vực là một khoảng không gian liên tục gồm nhiều sector/block để tách biệt dữ liệu.

## Phân vùng
- LBA (Logical Block Addressing): Là các sector được đánh số thứ tự (LBA 0, LBA 1, LBA 2...)
### MBR (Master Boot Record)
MBR là chuẩn cũ. Bảng phân vùng nằm tại LBA 0:
- Bootstrap Code (446 bytes): Đoạn mã khởi động nhỏ để nạp hệ điều hành từ phân vùng khởi động.
- Partition Table (64 bytes): Bảng mô tả tối đa 4 phân vùng chính (Primary Partitions). Mỗi entry chiếm 16 bytes chứa thông tin về loại phân vùng, sector bắt đầu và sector kết thúc.
- Boot Signature (2 bytes): Chữ ký kết thúc mang giá trị cố định 0xAA55.

### GPT (GUID Partition Table)
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
#### LBA 0 (Protective MBR) 
Bảng MBR giả để bảo vệ ổ đĩa, ngăn các công cụ quản lý đĩa cũ (chỉ đọc MBR) nhận nhầm ổ đĩa và ghi đè dữ liệu.
#### LBA 1 (Primary GPT Header)
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

#### LBA 2 đến LBA 33 (Partition Entries)
| Offset | Length | Contents |
| --- | --- | --- |
| `0x00` | 16 bytes | **Partition type GUID** (mixed endian) – mã định danh loại phân vùng (ví dụ: EFI System, Basic Data, Linux Filesystem...), giúp hệ điều hành biết mục đích sử dụng của phân vùng này. |
| `0x10` | 16 bytes | **Unique partition GUID** (mixed endian) – mã định danh duy nhất của riêng phân vùng này (mỗi phân vùng được tạo ra sẽ có một GUID ngẫu nhiên khác nhau để phân biệt). |
| `0x20` | 8 bytes | **First LBA** (little endian) – địa chỉ sector (LBA) bắt đầu của phân vùng trên ổ đĩa. |
| `0x28` | 8 bytes | **Last LBA** (little endian, tính bao gồm cả sector này, thường là số lẻ) – địa chỉ sector (LBA) kết thúc của phân vùng trên ổ đĩa. |
| `0x30` | 8 bytes | **Attribute flags** – các cờ thuộc tính điều khiển hành vi phân vùng (ví dụ: bit 0 báo phân vùng hệ thống bắt buộc, bit 60 thiết lập chế độ chỉ đọc/read-only, bit 62 ẩn phân vùng...). |
| `0x38` | 72 bytes | **Partition name** (tối đa 36 ký tự mã hóa UTF-16LE, kết thúc bằng ký tự null) – tên nhãn hiển thị do người dùng hoặc hệ thống đặt cho phân vùng. | 

#### Backup Partition Entries và Secondary GPT Header
Lưu một bản sao lưu của Partition Entries và GPT Header

### Hệ thống tệp
#### FAT32
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

#### NTFS
| Offset | Length | Contents |
| --- | --- | --- |
| Sector 0 | 1 sector | **Partition Boot Sector (`$Boot`)** – chứa BIOS Parameter Block (84 bytes đầu khai báo kích thước sector, cluster, tổng số sector) và tọa độ Cluster bắt đầu của `$MFT` (tại byte offset `0x30`), giúp hệ điều hành định vị bảng quản lý file ngay khi mount phân vùng. |
| Sector 1 | 8192 - Sector_Size bytes | **Bootstrap Code** – vùng chứa mã mồi khởi động NTLDR/BOOTMGR để nạp hệ điều hành Windows (cùng với Sector 0 tạo thành vùng siêu dữ liệu `$Boot`). |
| Byte 8192 (Cluster 2) | Phần lớn dung lượng phân vùng | **Data Area** – vùng lưu trữ nội dung dữ liệu thực tế của các file lớn (Non-resident data) và các file quản trị hệ thống ẩn như `$Bitmap` (theo dõi cluster trống), `$LogFile` (nhật ký giao dịch), `$MFTMirr` (bản sao 4 record đầu của `$MFT`)... |
| Cluster_MFT x Cluster_Size | 1024 bytes / record | **`$MFT` (Master File Table)** – bảng cơ sở dữ liệu trung tâm quản lý toàn bộ file và thư mục trên phân vùng; mỗi MFT Record lưu trữ các thuộc tính metadata (tên, quyền, thời gian, danh sách Data Runs) và chứa trực tiếp dữ liệu nếu file có kích thước nhỏ (< ~700 bytes, gọi là Resident data). |
| Ngay sau `$MFT` | ~12.5% dung lượng phân vùng | **MFT Zone** – vùng không gian trống được hệ thống ưu tiên giữ chỗ riêng ngay liền kề sau `$MFT` để bảng này có thể tự mở rộng liên tục khi tạo thêm file mới mà không bị phân mảnh (chỉ bị trưng dụng lưu dữ liệu thường khi phân vùng gần đầy). |
| Sector cuối cùng | 1 sector | **Backup Boot Sector** – bản sao dự phòng nguyên vẹn của Sector 0, luôn nằm ở sector vật lý cuối cùng của phân vùng để khôi phục khả năng truy cập ổ đĩa nếu Boot Sector chính bị hỏng. |

##### Siêu dữ liệu NTFS phục vụ điều tra
- `$MFT` (Master File Table):
    - Cơ chế lưu trữ: Phân bổ cố định 1024 bytes/bản ghi quản lý toàn bộ tệp và thư mục trên NTFS.
    - Cấu trúc `$DATA` (0x80):
        - Resident Data: Nội dung file nhỏ (thường < 700–800 bytes) lưu trực tiếp trong bản ghi MFT, không cấp phát cluster ngoài đĩa.
        - Non-Resident Data: File lớn hơn được lưu ở cluster ngoài; thuộc tính 0x80 chỉ lưu con trỏ cấp phát `Data Runs` (VCN/LCN).

- Alternate Data Streams (ADS):
    - Cho phép một file chứa nhiều luồng `$DATA` độc lập bên cạnh luồng mặc định (`<filename>:<stream_name>`).
    - Lưu trữ Metadata hệ thống (như luồng `:Zone.Identifier` lưu thông tin Mark-of-the-Web), hash, hoặc toàn bộ payload nhị phân/script (`.exe`, `.dll`, `.vbs`).
    - Kích thước file hiển thị trên Windows Explorer không đổi dù luồng phụ chứa dữ liệu; payload có thể được nạp và thực thi trực tiếp qua các tiến trình hệ thống (`wscript.exe`, `rundll32.exe`).

- `$UsnJrnl:$J` (Update Sequence Number Journal - Stream $J):
    - Cơ chế lưu trữ: Ghi nhật ký tuần tự (append-only) các sự kiện thay đổi trạng thái tệp theo thời gian thực.
    - Dữ liệu thu thập: Tên tệp, File Reference Number, Parent Entry Number, timestamp và Update Reasons (`FileCreate`, `FileDelete`, `DataExtend`, `Close`, v.v.).

#### Ext4
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

Các Block Group 1, 2, 3... có cấu trúc trên lặp lại. Để tiết kiệm dung lượng, Ext4 chỉ đặt bản sao của Superblock và GDT ở đầu các Group có số thứ tự là lũy thừa của 3, 5, 7. Các Group còn lại sẽ bắt đầu ngay bằng Data Block Bitmap.