## Forensics Git 2
Sau khi tải về và giải nén thì được file `disk.img`
Kiểm tra `disk.img` thì đây là một disk image sử dụng bảng phần vùng chuẩn MBR, gồm 3 phân vùng. Trong đó phân vùng 3 là lớn nhất nên có thể đây chính là phân vùng Root File System (/)
![image](img1.png)


Thực hiện tính `offset = Start_sector * Sector_size` (với MBR thì Sector_size=512) và mount phân vùng 3 ra file `mnt`
```
mkdir mnt
sudo mount -o loop,offset=584056832 disk.img mnt/
```


Di chuyển đến file `killer-chat-app`, tại đây có file client, server và thư mục logs. Kiểm tra thư mục logs thấy thiếu đi file 3.txt
=> file này có thể chứa flag và đã bị xóa đi
![image](img2)


Sử dụng các lệnh `git branch` `git log` không có gì nên tiến hành điều tra sâu hơn trong `.git`. Tại đây tìm thấy lịch sử commit đã bị xóa đi trong file `.git/logs/HEAD`
![image](img3)


Khôi phục lại trạng thái commit `e80b38b3322a5ba32ac07076ef5eeb4a59449875` thì tại thư mục `logs` xuất hiện trở lại `3.txt`. Trích xuất file này và lấy được flag
```
git reset --hard e80b38b3322a5ba32ac07076ef5eeb4a59449875

cat 3.txt

#Rex: Meet at the old arcade basement for the secret hideout.
#Jay: Ask Rusty at the door and use password picoCTF{g17_r35cu3_16ac6bf3}.
#Rex: Bring the decoder map so we can plan the route.
```

FLAG: **picoCTF{g17_r35cu3_16ac6bf3}**
