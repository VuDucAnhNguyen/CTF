# Lý thuyết
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
### MBR
MBR (Master Boot Record) là chuẩn cũ. Bảng phân vùng nằm tại LBA 0:
- Bootstrap Code (446 bytes): Đoạn mã khởi động nhỏ để nạp hệ điều hành từ phân vùng khởi động.
- Partition Table (64 bytes): Bảng mô tả tối đa 4 phân vùng chính (Primary Partitions). Mỗi entry chiếm 16 bytes chứa thông tin về loại phân vùng, sector bắt đầu và sector kết thúc.
- Boot Signature (2 bytes): Chữ ký kết thúc mang giá trị cố định 0xAA55.

### GPT
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
- LBA 0 (Protective MBR): bảng MBR giả để bảo vệ ổ đĩa, ngăn các công cụ quản lý đĩa cũ (chỉ đọc MBR) nhận nhầm ổ đĩa và ghi đè dữ liệu.
- LBA 1(Primary GPT Header): Đầu trang chính, chứa thông tin định danh ổ đĩa (GUID), kích thước sector, vị trí và số lượng ô chứa phân vùng, kèm mã kiểm tra lỗi (CRC32).
- LBA 2 đến LBA 33 (Partition Entries): Mảng chứa danh sách các phân vùng (thường hỗ trợ tối đa 128 phân vùng trên Windows). Mỗi entry dài 128 bytes chứa tên, GUID loại phân vùng, khoảng LBA bắt đầu và kết thúc.
- 