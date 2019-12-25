# IO
## File maps_generator/config.json
- Chứa json object:
	- Một mảng chứa các bộ cấu hình. Mỗi bộ cấu hình gồm:
		- NMaps: Số bản đồ được sinh ra ứng với bộ cấu hình
		- mapsName: Tên thư mục chứa các bản đồ ứng với bộ cấu hình
		- ratio: Tỉ lệ "thưa hoá" mật độ FSO
		- NPivot: Số phần tử trụ
		- Nr: Số hàng của bản đồ
		- Nc: Số cột của bản đồ
		- pivot: Mảng chứa thông tin các phần tử trụ. Mỗi phần tử gồm
			- coordinates: Toạ độ
				- r: Chỉ số hàng
				- c: Chỉ số cột
			- influence: Độ ảnh hưởng của xác suất
				- r: Tốc độ giảm ảnh hưởng. (Ví dụ, với r bằng 1 thì mật độ thay đổi tuyến tính)
				- c: Xác suất có FSO tại ô (r, c)

## Thư mục maps/
- Chứa các bản đồ được sinh ra
	- Mỗi thư mục con ứng với một bộ cấu hình. Trong mỗi thư mục con chứa các file json tương ứng với một bản đồ:
		- NFSO: Số FSO
		- FSO: Mảng các thuộc tính FSO
			- r: Toạ độ hàng FSO
			- c: Toạ độ cột FSO
			- l: Toạ độ chiều thứ 3 của FSO
		- throughput: Mảng 2 chiều, phần tử (i, j) là thông lượng truyền tin giữa FSO thứ i và FSO thứ j.

# Visualize
- Vào thư mục visualize/, chạy lệnh `python visualize_fso_map.py file_map.json`.

# Thuật toán sinh
- File maps_generator/main.py
- Thuật toán:
	- Tính hệ số ảnh hưởng của mỗi pivot lên một ô (ir, ic) theo công thức: I = 1 / (d ^ r).
		- d là khoảng cách giữa pivot và ô (ir, ic)
		- r là hệ số thể hiện tốc độ giảm ảnh hưởng
	- Xác suất ô (ir, ic) có FSO: P = tổng c * I / (S * ratio) với mọi pivot
		- c là xác suất pivot chứa FSO
		- I là hệ số ảnh hưởng của pivot tương ứng lên ô (ir, ic)
		- S là tổng hệ số ảnh hưởng của mọi pivot
		ratio là tham số phụ, để "thưa hoá" mật độ FSO
	- Xác định ô (ir, ic) có FSO không
		- Sinh ngẫu nhiên 1 số rand trong khoảng [0, 1]
		- Nếu rand < P thì ô (ir, ic) có FSO