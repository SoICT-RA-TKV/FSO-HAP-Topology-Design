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