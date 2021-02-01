# Giới thiệu
- Chương trình sinh dữ liệu đầu vào cho bài toán thiết kế và triển khai mạng FSO.

# Requirements
- Chạy lệnh `pip install -r requirements.txt` để cài các modules cần thiết

# Chạy chương trình
- Chạy lệnh `python src/main.py` để thực hiện tất cả công việc, hoặc chạy từng bước theo hướng dẫn phía dưới.

# Sinh bản đồ
## Cấu hình bản đồ
- File config đặt trong thư mục data, hoặc thư mục con của thư mục data
```
	# Kich thuoc map: hang x cot (đơn vị km)
	20 20
	# Kich thuoc 1 o: cao x rong (đơn vị km)
	1 1
	# So pivot
	4
	# Danh sach pivot: toa do (hang, cot) tam anh huong (toc do giam, anh huong tai tam)
	20 20 1 0.1
	1 20 1 0.1
	1 1 1 0.45
	20 1 1 0.45
	# Ti le thua hoa (tăng tỉ lệ này nếu muốn giảm mật độ fso)
	2
	# Ten map (map sinh ra được lưu dưới dạng data/$(Ten map)/gfso_$(số fso)_$(chỉ số phụ).txt)
	GFSO_01
	# So map can sinh voi config nay
	5
```

## Thuật toán sinh bản đồ
- Tính hệ số ảnh hưởng của mỗi pivot lên một ô (ir, ic) theo công thức: I = 1 / (d ^ r).
 + d là khoảng cách giữa pivot và ô (ir, ic)
 + r là hệ số thể hiện tốc độ giảm ảnh hưởng
- Xác suất ô (ir, ic) có FSO: P = tổng c * I / (S * ratio) với mọi pivot
 + c là xác suất pivot chứa FSO
 + I là hệ số ảnh hưởng của pivot tương ứng lên ô (ir, ic)
 + S là tổng hệ số ảnh hưởng của mọi pivot
 + ratio là tham số phụ, để "thưa hoá" mật độ FSO
- Xác định ô (ir, ic) có FSO không
 + Sinh ngẫu nhiên 1 số rand trong khoảng [0, 1]
 + Nếu rand < P thì ô (ir, ic) có FSO
	
# Phân cụm
- Chạy lệnh `python clustering.py [ten_file]`.
 + Chương trình `clustering` sẽ lấy `ten_file` mặc định là `data` nếu không truyền tham số này.
 + Nếu `ten_file` là đường dẫn đến 1 folder, chương trình sẽ quét toàn bộ các bản đồ fso chứa trong thư mục đó và thực hiện phân cụm.
 + Tên bản đồ fso bắt buộc có tiền tố `ground_fso` và đuôi `.txt`.
 + Output là file có tên giống bản đồ fso, nhưng thay tiền tố `ground_fso` thành tiền tố `clustering`.

# Visualize
- Chạy lệnh `python visualizer.py [ten_file]`.
 + Chương trình `visualizer` sẽ lấy `ten_file` mặc định là `data` nếu không truyền tham số này.
 + Nếu `ten_file` là đường dẫn đến 1 folder, chương trình sẽ quét toàn bộ các bản đồ fso và bản đồ fso đã phân cụm trong thư mục đó và thực hiện phân cụm.
 + Tên bản đồ fso bắt buộc có tiền tố `ground_fso` và đuôi `.txt`.
 + Tên bản đồ fso đã phân cụm có tiền tố `clustering` và đuôi `.txt`.
 + Output là file có tên giống bản đồ, nhưng thay đuôi `.txt` thành đuôi `.png`.