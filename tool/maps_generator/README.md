# File config
1. Định dạng: json
2. Cấu trúc:
- Mảng các cấu hình
- Mỗi cấu hình gồm
 + NPivot: Số chốt
 + NMaps: Số maps sinh ra từ cấu hình
 + mapsName: Tên cấu hình
 + Nr: Số hàng (chiều cao bản đồ)
 + Nc: Số cột (chiều rộng bản đồ)
 + ratio: Tỉ lệ "thưa hoá" bản đồ
 + pivot: Cấu hình các chốt
  - coordinates: toạ độ chốt gồm r, c, l
  - influence: thông số về mức độ ảnh hưởng
   + r: Tốc độ giảm ảnh hưởng khi đi ra xa chốt
   + c: Mức độ ảnh hưởng cơ sở (= xác suất có FSO tại điểm chốt)

# Thuật toán sinh bản đồ
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