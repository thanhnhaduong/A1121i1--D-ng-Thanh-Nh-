# 7. Bảng cân bằng Stress Units & Throughput

> ⚠ Các con số SU của **Create gốc** (Steam Engine, Water Wheel…) phụ thuộc config
> (`create-common.toml`) và có thể khác giữa các bản. Các con số của **Titan Aerospace** là do
> mod định nghĩa nên luôn đúng. Hãy kiểm tra lại giá trị Create trước khi công bố modpack.

## 7.1. Tham chiếu máy phát (Create 0.5.1, config mặc định)

| Nguồn | Capacity (su/RPM) | RPM thường | SU cấp được |
|---|---:|---:|---:|
| Water Wheel | 16 | 8 | 128 |
| Large Water Wheel | 128 | 8 | 1 024 |
| Windmill (16 sail) | 512 | 8 | 4 096 |
| **Steam Engine** (nồi hơi max) | 1 024 | 16 | **16 384** |
| Nồi hơi 9×9×9 max (18 engine) | — | 16 | **≈ 294 912** |

## 7.2. Stress của máy Titan Aerospace

| Máy | Impact (SU/RPM) | RPM vận hành | SU / máy |
|---|---:|---:|---:|
| Crustal Drilling Rig | 1 024 | 128 | 131 072 |
| Acid Leaching Vat | 32 | 90 | 2 880 |
| Hydro Cyclone | 64 | 64 | 4 096 |
| Chlorination Reactor | 256 | 64 | 16 384 |
| Distillation Column (mỗi tầng) | 96 | 96 | 9 216 |
| Kroll Retort | 512 | 96 | 49 152 |
| Electrolysis Cell | 384 | 128 | 49 152 |
| Vacuum Arc Remelter | 256 | 128 | 32 768 |
| Air Liquefier | 384 | 128 | 49 152 |
| Cryo Mixing Chamber | 128 | **128 cố định** | 16 384 |
| Titan Forge | 192 | 64 | 12 288 |
| Reinforced Mechanical Crafter | 16 | **256** | 4 096 |

## 7.3. Ngân sách công suất toàn nhà máy

| Cụm | Số máy | Tổng SU |
|---|---:|---:|
| Khoan & nghiền | 8 rig + 24 cặp crushing wheel | 1 073 152 |
| Ngâm / rửa | 6 vat + 8 cyclone | 50 048 |
| Hóa chất (clo hóa, chưng cất, Kroll, điện phân) | 12 + 30 tầng + 16 + 8 | 1 652 736 |
| Nấu chảy | 20 VAR | 655 360 |
| Khí hóa lỏng & nhiên liệu | 4 liquefier + 4 cryo mixer | 262 144 |
| Rèn vỏ | 6 Titan Forge | 73 728 |
| Mảng crafter 15×15 | 225 | 921 600 |
| **ĐỈNH (chạy tất cả song song)** | | **≈ 4 689 000 SU** |
| **THỰC TẾ (chia pha bằng Clutch)** | | **≈ 2 800 000 SU** |

### Quy ra số máy phát

| Kịch bản | Steam Engine | Nồi hơi 9×9×9 max |
|---|---:|---:|
| Đỉnh, không chia pha | 287 | **16** |
| Chia pha (khuyến nghị) | 171 | **10** |
| Chỉ để chạy mảng crafter | 57 | 4 |

> 10 nồi hơi 9×9×9 cần ≈ 180 Steam Engine, ≈ 180 Water Pump nuôi nước, và một farm nhiên liệu
> (thường là Sugar Cane → Blaze Cake hoặc dầu từ addon). **Đây chính là "mega-factory"** mà đề
> bài yêu cầu — nó chiếm nhiều thời gian hơn cả dây chuyền titan.

## 7.4. Ngân sách thời gian (mục tiêu ~90 phút mỗi pha)

| Pha | Công việc | Máy | Thời gian |
|---|---|---|---|
| 1a Bootstrap | 256 thỏi qua RNG 0.8 % | 4 rig + 16 cyclone | ≈ 30 phút |
| 1b Công nghiệp | 22 000 thỏi Titanium | 8 rig + 12 reactor + 16 retort + 20 VAR | ≈ 90 phút |
| 2 Linh kiện | 17 000 plate + 8 động cơ | 6 Titan Forge | ≈ 70 phút |
| 2 Nhiên liệu | 6 144 000 mB | 4 liquefier + 4 mixer | ≈ 60 phút |
| 3 Lắp ráp | 64 hull module | mảng 15×15 | ≈ 20 phút |
| 3 Nạp & phóng | 6.1 M mB + đếm ngược | 8 umbilical | ≈ 4 phút |
| | | **Tổng vận hành** | **≈ 4.5 giờ** |
| | | **Tổng kể cả xây dựng** | **40 – 80 giờ** |

## 7.5. Nút xoay cân bằng (config)

```toml
[balance]
oreChanceMultiplier      = 1.0   # nhân vào 0.8 % của Hydro Cyclone
stressMultiplier         = 1.0   # nhân vào toàn bộ impact của mod
rocketTitaniumRequirement= 1.0   # 0.25 = "chế độ nhẹ nhàng" cho modpack nhỏ
processingTimeMultiplier = 1.0
[balance.gregtech_mode]
enabled = false                  # true: tỉ lệ 0.5 %, thời gian ×1.5, tắt Đường A sau khi
                                 #       xây xong nhà máy hóa chất (không cho bootstrap vô hạn)
```
