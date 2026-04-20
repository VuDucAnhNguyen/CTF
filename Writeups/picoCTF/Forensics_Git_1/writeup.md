## Forensics Git 1
Sau khi tải về và giải nén thì được file `disk.img`
Kiểm tra `disk.img` thì đây là một disk image sử dụng bảng phần vùng chuẩn MBR, gồm 3 phân vùng. Trong đó phân vùng 3 là lớn nhất nên có thể đây chính là phân vùng Root File System (/)
![image](img1.png)


Thực hiện tính `offset = Start_sector * Sector_size` (với MBR thì Sector_size=512) và mount phân vùng 3 ra file `mnt`
```
mkdir mnt
sudo mount -o loop,offset=584056832 disk.img mnt/
```


Do đề bài có nhắc đến git khiến mình nghĩ đến tìm file `.git` trong ổ đĩa:
```
find . -name ".git" -type d 2>/dev/null        
#./mnt/home/ctf-player/Code/secrets/.git
```

Di chuyển đến file `secrets`, sử dụng `git log` để xem lại lịch sử commit thì thấy có hành động thêm và xóa flag
![image](https://hackmd.io/_uploads/S1eews82-e.png)


Khôi phục lại trạng thái commit `177789af0b300e043ea8f54ea57d6cee352291ae` thì xuất hiện file flag.txt, trích xuất file này thu được flag
```
git reset --hard 177789af0b300e043ea8f54ea57d6cee352291ae

cat flag.txt
#picoCTF{g17_r3m3mb3r5_d4ddf904}
```

FLAG: **picoCTF{g17_r3m3mb3r5_d4ddf904}**
