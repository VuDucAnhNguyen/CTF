# Lý thuyết
Các file event log của Windows lưu tại `%SystemRoot%\System32\winevt\Logs`. Cấu trúc 1 file `.evtx` như sau
```
+-------------------------------------------------------------+
| File Header (4,096 bytes = 4 KB)                            |
+-------------------------------------------------------------+
| Chunk 0 (65,536 bytes = 64 KB)                              |
|   ├── Chunk Header (512 bytes)                              |
|   ├── Event Record 1 (`2A 2A 00 00` ... 4-byte Size ở cuối) |
|   ├── Event Record 2 (`2A 2A 00 00` ... 4-byte Size ở cuối) |
|   ├── ...                                                   |
|   └── Vùng trống (tới hết byte thứ 65,535 của Chunk)        |
+-------------------------------------------------------------+
| Chunk 1 (64 KB)                                             |
| ...                                                         |
+-------------------------------------------------------------+
| ...                                                         |
+-------------------------------------------------------------+
```
- **File Header** (4,096 bytes): Chỉ xuất hiện ở đầu file `.evtx`. Lưu chữ ký `ElfFile\x00` (`0x456C6646696C6500`), số phiên bản, tổng số chunk hiện có.
- **Chunk** (65536 bytes/chunk): `.evtx` gom các event thành từng khối 64 KB.
  - Chunk Header (512 bytes): Bắt đầu bằng chữ ký `ElfChnk\x00` (`0x456C6643686E6B00`), lưu EventRecordID đầu/cuối của chunk, LogRecordNumber đầu/cuối, con trỏ offset tới vùng trống cuối chunk (FreeSpaceOffset), bảng băm chuỗi/template nội bộ và ChunkChecksum.
  - Vùng Event Records: Nằm từ sau byte thứ 512 của chunk cho đến hết chunk.
  
Cấu trúc 1 event record
| Offset | Length | Content |
| - | -| - |
| `0x00` | 4 bytes | Signature - Magic bytes `2A 2A 00 00` |
| `0x04` | 4 bytes | Size - Tổng kích thước của bản ghi event (bao gồm cả 4 bytes lặp lại ở cuối record để khóa đuôi) |
| `0x08` | 8 bytes | EventRecordID - Số thứ tự định danh duy nhất của sự kiện trong log |
| `0x10` | 8 bytes | TimeCreated - Thời điểm ghi nhận sự kiện theo định dạng Windows FILETIME |
| `0x18` | Biến thiên | BinXML Payload -Nội dung chi tiết của sự kiện (Event ID, Provider, Channel, Computer, UserData/EventData) được nén dưới dạng BinXML.