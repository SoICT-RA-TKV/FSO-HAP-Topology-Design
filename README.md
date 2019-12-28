# Requirements
- Chạy lệnh `pip install -r requirements.txt` để cài các modules cần thiết

# Sinh bản đồ
## Cấu hình bản đồ
1. File ground_fso_generator.json
2. Cấu trúc:
- Mảng các cấu hình
- Mỗi cấu hình gồm
 + NPivot: Số chốt
 + NMaps: Số maps sinh ra từ cấu hình
 + mapName: Tên cấu hình
 + Nr: Số hàng (chiều cao bản đồ)
 + Nc: Số cột (chiều rộng bản đồ)
 + ratio: Tỉ lệ "thưa hoá" bản đồ
 + pivot: Cấu hình các chốt
  - coordinates: toạ độ chốt gồm r, c, l
  - influence: thông số về mức độ ảnh hưởng
   + r: Tốc độ giảm ảnh hưởng khi đi ra xa chốt
   + c: Mức độ ảnh hưởng cơ sở (= xác suất có FSO tại điểm chốt)
3. Output
- Bản đồ được sinh ra trong thư mục `data`
- Các bản đồ thuộc 1 bộ cấu hình được đặt trong thư mục có tên là `mapName` của bộ cấu hình đó.
- Mỗi bản đồ là 1 file `.txt` có tiền tố là `ground_fso`.

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