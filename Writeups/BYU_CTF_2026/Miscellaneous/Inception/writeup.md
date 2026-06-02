## Inception
### Đề bài
I found this weird file on my computer. I tried opening it, but there were some problems.

### Giải
Sau khi tải về thì được file `inception`. Sử dụng file để kiểm tra thì file có header của ảnh PNG nhưng mở ra lại là file PDF chứa 1 phần flag
![image](img1.png)

Sử dụng hxd để cắt file ảnh ra thì được phần tiếp theo của flag
![image](image.png)

Trong file inception còn chứa file zip bên trong, trích xuất và giải nén thì được `data.bin` chứa phần còn lại của flag
![image](img2.png)
![image](img3.png)

FLAG: **byuctf{wh4t_th3_fr3ak}**