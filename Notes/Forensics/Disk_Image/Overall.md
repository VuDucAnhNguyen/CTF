# Lý thuyết
## Các loại ảnh đĩa
### Nhóm ảnh thô (Raw / Bit-stream Image): `.raw`, `.img`, `.dd`
  - Là bản sao chép y nguyên từng bit (1:1) từ ổ đĩa vật lý hoặc phân vùng ra file. Không có header mô tả, không nén, không mã hóa.
  - Dung lượng file bằng đúng dung lượng ổ đĩa gốc. Có thể dùng trực tiếp các công cụ cấp thấp như dd, The Sleuth Kit, hoặc mở bằng HxD để soi từng byte mà không cần giải mã vỏ bọc.

### Nhóm ảnh đĩa máy ảo: `.vmdk` (VMware), `.vhd` / `.vhdx` (Hyper-V), `.qcow2` (QEMU/KVM)

  - Sinh ra để phần mềm ảo hóa giả lập một ổ cứng.
  - Đặc điểm: Phần đầu file chứa một đoạn Header mô tả thông số phần cứng ảo (số sector, cylinder, thông tin snapshot...). Sử dụng cơ chế cấp phát động: nó bỏ qua các vùng trống toàn số 0 và dùng bảng ánh xạ nội bộ để quản lý. Không thể tính offset vật lý trực tiếp trên file .vmdk.
### Nhóm ảnh điều tra số chuyên dụng: `.e01` (EnCase) và `.ad1` (FTK Imager)
  - `.e01` (Expert Witness Format): Là ảnh sao chép vật lý 1:1, được bọc thêm lớp vỏ điều tra số: có nén dữ liệu, chia nhỏ thành nhiều mảnh (E01, E02...), và lưu kèm metadata.
  - `.ad1` (AccessData Logical Image): là ảnh logic (Logical Image), không phải ảnh vật lý. Thay vì sao chép cả ổ đĩa từ sector 0, công cụ chỉ gom nhặt một số thư mục/file cụ thể rồi đóng gói lại kèm metadata cơ bản của các file đó.

## Đơn vị lưu trữ
- **Sector**: Đơn vị vật lý/cơ bản nhỏ nhất mà ổ đĩa đọc hoặc ghi.
- **Block**: Đơn vị dữ liệu logic dùng cho thao tác đọc/ghi I/O của hệ điều hành, cơ sở dữ liệu hoặc tầng lưu trữ, có kích thước bằng hoặc là bội số của sector.
- **Cluster**: Nhóm gồm nhiều sector liền kề do hệ thống tệp tin quản lý; là đơn vị nhỏ nhất được cấp phát khi lưu một tệp tin.
- **Partition**: Phân vùng logic lớn chia một ổ đĩa vật lý thành các khu vực độc lập. mỗi khu vực là một khoảng không gian liên tục gồm nhiều sector/block để tách biệt dữ liệu.

# Các phương pháp và công cụ điều tra Disk Image
## The Sleuth Kit (TSK)
### Volume Layer (Tầng Phân vùng / Quản lý phương tiện)
Đây là lớp ngoài cùng, chuyên xử lý cấu trúc phân vùng cấp cao của toàn bộ ổ đĩa (như chuẩn MBR hay GPT). Giúp xác định ổ đĩa cứng được chia thành bao nhiêu phân vùng, vị trí bắt đầu (start sector) và kết thúc (end sector) của từng phân vùng nằm ở đâu.

Tiền tố công cụ: `mm-` (Media Management)
- `mmls`: Liệt kê danh sách các phân vùng trên ảnh đĩa (tương tự lệnh xem bảng phân vùng).
- `mmstat`: Hiển thị kiểu hệ thống phân vùng (DOS/MBR, GPT,...) đang sử dụng.
```
mmls [file_name]
mmstat [file_name]
```

### File System Layer (Tầng Hệ thống tệp)
Lớp này xử lý các thông số tổng quan của hệ thống tệp đang chạy trên phân vùng đó (như NTFS, FAT32, Ext4, UFS). Đọc các thông số cấu hình chung của hệ thống tệp (kích thước cluster/block, tổng số cluster, tên volume, thời gian mount gần nhất).

Tiền tố công cụ: `fs-`
- `fsstat`: Hiển thị thông tin tổng quan và thống kê chi tiết của hệ thống tệp. (Lưu ý: cần chỉ định điểm lệch sector qua tham số -o, có thể sử dụng các cờ ).
```
fsstat -o [start_offset_of_partition] [file_name]
```

### Content Layer / Data Unit Layer (Tầng Khối dữ liệu / Nội dung)
Lớp này quản lý các đơn vị lưu trữ cơ bản (được gọi là block trong Linux/Unix hoặc cluster trong Windows) nơi chứa nội dung thực tế của tệp. Cho phép đọc nội dung thô của từng khối dữ liệu riêng lẻ, hoặc quét các khối chưa được cấp phát để tìm dữ liệu bị xóa, dữ liệu thừa (slack space).

Tiền tố công cụ: `blk-` (Block)
- `blkcat`: Xem nội dung thô của một block/cluster cụ thể.
- `blkls`: Liệt kê nội dung của các khối chưa phân phối (vùng trống/dữ liệu đã xóa) để phục vụ việc tìm kiếm nội dung.
- `blkstat`: Xem trạng thái chi tiết của một block (đã cấp phát hay chưa).

### Metadata Layer (Tầng Siêu dữ liệu / Inode / MFT Record)
Mỗi tệp hoặc thư mục trên hệ thống tệp đều có một cấu trúc siêu dữ liệu đại diện riêng (gọi là Inode trong Linux hoặc MFT Record trong NTFS). Lớp này quản lý các cấu trúc đó. Lưu trữ thông tin mô tả chi tiết của tệp (kích thước, thời gian tạo/sửa đổi, quyền hạn, và danh sách các con trỏ trỏ tới các khối dữ liệu thực tế).

Tiền tố công cụ: `i-` (Inode / Index)
- `istat`: Hiển thị toàn bộ thông tin chi tiết (metadata) của một record/inode cụ thể, bao gồm các sector mà nó chiếm giữ.
- `icat`: Trích xuất nội dung của một file trực tiếp dựa vào số hiệu metadata (inode hoặc record number) của nó.
- `ils`: Liệt kê danh sách các metadata (đặc biệt hữu ích với các metadata chưa phân phối/đã xóa).
```
istat -o [start_offset_of_partition] [file_name] [inode]
icat -o [start_offset_of_partition] [file_name] [inode]
istat -o [start_offset_of_partition] [file_name] [inode]
```

### File Name Layer (Tầng Tên tệp)
Quản lý tên hiển thị của file và thư mục nằm trong cấu trúc cây thư mục. Lệnh có thể sử dụng kết hợp với các cờ tương tự ls, find.

Tiền tố công cụ: `f-`
- `fls`: Liệt kê tên các file và thư mục (những file có dấu `*` ở trước là file đã bị xóa).
- `ffind`: Tìm kiếm tên file dựa vào số hiệu metadata tương ứng.
```
fls -o [start_offset_of_partition] [flag] [file_name] [inode]
```

VD: [RESURRECTION (Operation Eclipse Void)](../../../Writeups/HI_Cyber_Con_2026/Forensics/RESURRECTION_(Operation_Eclipse_Void)/writeup.md)

