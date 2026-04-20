| Định dạng | Chữ ký (đầu file, hex) | Chữ ký cuối file (footer) | Phần mở rộng |
| --- | ---------------------------- | ---------- | :-----------: |
|  PNG  | `89 50 4E 47 0D 0A 1A 0A` | Chunk `IEND` + CRC: <br> `00 00 00 00 49 45 4E 44 AE 42 60 82` | .png |
|  JPEG  | `FF D8 FF E0` <br> `FF D8 FF E1` (JFIF/Exif) | `FF D9` | .jpg, .jpeg, .jfif |
|  PDF  | `25 50 44 46` (“%PDF”) | `25 25 45 4F 46` (`%%EOF`) | .pdf |
|  ZIP  | `50 4B 03 04` (”PK/03/04”) <br> `50 4B 05 06` <br> `50 4B 07 08`  | EOCD signature: `50 4B 05 06` | .zip, .jar, .apk, <br> .docx, .pptx, .xlsx… |
|  DOCX  | Cùng chữ ký với ZIP | EOCD: `50 4B 05 06` | .docx, .pptx, .xlsx |
|  ELF  | `7F 45 4C 46` (“.ELF”) |  | (Linux executable) |
|  WAV  | `52 49 46 46 .. 57 41 56 45` (“RIFF....WAVE”) | Không có footer cố định (dựa vào kích thước) | .wav |
|  MP4  | `00 00 00 ?? 66 74 79 70` (“ftyp” tại offset 4) | Không có footer riêng (dựa vào box sizes) | .mp4, .m4a, .mov |
|  RAR (v4)  | `52 61 72 21 1A 07 00` (“Rar!”) | `00 00 00 00` sau block cuối | .rar |
|  RAR (v5)  | `52 61 72 21 1A 07 01 00` | Tương tự v4 | .rar |
|  ISO9660  | Ở offset 0x8001 có chuỗi `43 44 30 30 31` (“CD001”) |  | .iso |
|  EXE  | `4D 5A` (”MZ”) |  | .exe |
|  GIF  | `47 49 46 38 37 61` (GIF87a) <br> `47 49 46 38 39 61` (GIF89a) |  | .gif |
|  BMP  | `42 4D` ("BM") |  | .bmp |
|  7-Zip  | `37 7A BC AF 27 1C` |  | .7z |
|  WEBP  | `52 49 46 46 .. .. .. .. 57 45 42 50` ("RIFF....WEBP") |  | .webp |
|  GZIP  | `1F 8B` |  | .gz |
|  SQLite  | `53 51 4C 69 74 65 20 66 6F 72 6D 61 74 20 33 00` ("SQLite format 3") |  | .sqlite, .db |
|  JAVA CLASS  | `CA FE BA BE` |  | .class |
|  TXT  | `EF BB BF` |  | .txt |
|  OGG  | `4F 67 67 53` ("OggS") |  | .ogg, .oga, .ogv |
|  FLAC  | `66 4C 61 43` ("fLaC") |  | .flac |
