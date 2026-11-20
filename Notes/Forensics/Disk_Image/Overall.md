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