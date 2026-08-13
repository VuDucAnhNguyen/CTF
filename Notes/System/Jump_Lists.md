## Lý thuyết
Jump Lists là một cơ chế của Windows dùng để lưu lịch sử và thông tin truy cập của người dùng đối với từng ứng dụng. 

VD: Khi bạn nhấp chuột phải vào biểu tượng của một ứng dụng trên Taskbar hoặc Start Menu, bạn sẽ thấy danh sách các file gần đây hoặc được ghim, đây chính là Jump Lists.

- Bên trong Jump List có thể chứa:
    - danh sách file đã mở
    - đường dẫn đầy đủ (Full Path)
    - thời gian truy cập
    - thời gian sửa
    - thời gian tạo
    - số lần mở
    - Volume Serial Number
    - MAC Address của ổ mạng (đôi khi)
    - thông tin Shortcut (LNK)
    - AppID
- Jump Lists thực chất là OLE Compound File (OLE CF) bên trong chứa nhiều stream, môi stream là một file LNK (shortcut)
    - DestList lưu trữ: 
        - Entry ID
        - AppID
        - MRU (Most Recently Used)
        - số lần mở
        - thời gian mở cuối
        - đường dẫn

### AutomaticDestinations
Đây là loại jump Lists phổ biến nhất, được Windows tự động tạo khi người dùng mở file, tên file là AppID của ứng dụng.

VD: `f01b4d95cf55d32a.automaticDestinations-ms`

Thường được lưu tại: `%APPDATA%\Microsoft\Windows\Recent\AutomaticDestinations\`

### CustomDestinations
Jump Lists do một số ứng dụng tự quản lý.

Thường được lưu tại: `%APPDATA%\Microsoft\Windows\Recent\CustomDestinations\`

## Các phương pháp và công cụ điều tra Jump Lists
### JLECmd.exe (Eric Zimmerman's tools)
Công cụ phân tích Jump Lists, thực hiện trích xuất các file `.lnk` bên trong và tổng hợp dữ liệu

Trích xuất dữ liệu và xuất file excel:

```
.\JLECmd.exe -f "[file_name]" --csv "[output_folder]"
```


VD: [TranscendentRenovation](../../Writeups/L3akCTF_2026/Forensics/TranscendentRenovation/writeup.md)

### Một số tool khác:
- strings
- oletools (olebrowse)