# 4. GIAI ĐOẠN 2 — Chế tạo linh kiện & 3 định luật vật lý

Ba linh kiện chính, mỗi cái gắn với một định luật và một kiểu rủi ro khác nhau:

| Linh kiện | Định luật | Biến số người chơi phải giữ | Hình phạt |
|---|---|---|---|
| Vỏ Titan (`titanium_plate`) | Nhiệt động lực học | Nhiệt độ lò ≥ ngưỡng, **liên tục** | Phôi → `iron_slag` |
| Nhiên liệu lỏng | Động lực học chất lưu | RPM bơm = 128 ± 4 | **NỔ** |
| Động cơ phản lực | Động năng học | Tốc độ = 256 RPM + đủ SU | Phôi hỏng, mất nguyên liệu |

---

## 4.1. Nhiệt động lực học — Rèn vỏ Titan

### Mô hình

Titan chỉ dẻo ở khoảng 900–1100 °C. Dưới ngưỡng đó nó giòn, và nếu phôi nguội giữa chừng thì
tạp chất sắt kết tinh lại → mẻ thành xỉ. Mod mô phỏng bằng một biến **`integrity` (độ toàn vẹn)**
thay vì mô phỏng nhiệt độ tuyệt đối.

```
ta:titan_forge  — 5×3×5, 192 SU/RPM, 600 tick/mẻ
  Bên dưới: 9× Blaze Burner nối qua ta:blaze_burner_manifold
  Bao quanh: ta:thermal_insulation_casing (giảm 50 % tốc độ mất toàn vẹn)
```

### Công thức (chạy mỗi tick khi đang có mẻ)

```
heatScore   = Σ burner:  SEETHING → 2 | KINDLED → 1 | còn lại → 0     (tối đa 18)
deficit     = REQUIRED_HEAT (18) − heatScore
insulation  = có thermal_insulation_casing đủ 4 mặt ? 0.5 : 1.0

if deficit > 0:  integrity -= deficit × 1.5 × insulation
else:            integrity += 0.25            // hồi phục CHẬM hơn 6 lần
integrity = clamp(integrity, 0, 100)

if integrity <= 0  →  FAIL: nhả 2× ta:iron_slag, hủy phôi, phát âm thanh fizz
```

### Ý nghĩa gameplay (thời gian ân hạn)

| Tình huống | deficit | Mất/tick (có cách nhiệt) | Thời gian tới khi hỏng |
|---|---:|---:|---|
| 1 burner tụt SEETHING → KINDLED | 1 | 0.75 | **133 tick ≈ 6.6 s** |
| Hết Blaze Cake, cả 9 burner còn lửa thường | 9 | 6.75 | **15 tick ≈ 0.75 s** |
| Nguồn cấp Blaze Cake đứt hẳn (burner tắt) | 18 | 13.5 | **7 tick ≈ 0.35 s** |

⇒ Người chơi **bắt buộc** phải xây:
1. Dây chuyền Blaze Cake tự động (Blaze farm + Mixing + Compacting),
2. Kho đệm (Vault + Stockpile Switch) để nạp burner liên tục,
3. Redstone interlock: nếu kho đệm < 30 % thì **không cho** phôi mới vào lò
   (dùng Stockpile Switch → Redstone Link → Deployer/Belt gate).

Bài học thiết kế: *"đừng khởi động mẻ mới khi chưa chắc nuôi nổi nó tới cuối."*

---

## 4.2. Động lực học chất lưu — Nhiên liệu tên lửa

### Hóa học thật

Động cơ LH₂/LOX chạy ở tỉ lệ khối lượng O:H ≈ **6:1**. Quy ra thể tích
(ρ_LOX = 1141 kg/m³, ρ_LH₂ = 71 kg/m³):

```
V_LOX : V_LH₂ = (6/1141) : (1/71) = 1 : 2.68
⇒ Công thức mod: 1000 mB LOX + 2680 mB LH₂ → 3000 mB Liquid Rocket Fuel
```

### Mô hình áp suất

Create không có khái niệm áp suất, nên mod định nghĩa:

```
P(bar) = |RPM| / 128 × 40        // 128 RPM ⇔ 40 bar danh định
```

Công thức nhiên liệu khai báo `requiredRpm = 128`, `tolerance = 4` ⇔ **38.75 – 41.25 bar**.

| Vùng | RPM | Hiện tượng |
|---|---|---|
| Quá thấp | < 124 | LH₂ không sương hóa → đọng thành vũng → **kích nổ chậm (deflagration)** |
| Ổn định | 124 – 132 | Trộn đều, ra fuel |
| Quá cao | > 132 | Quá áp buồng trộn → **BLEVE** (nổ mạnh + cháy) |

Chi tiết công thức tích lũy `instability` và sức nổ: [06-risk-mechanics.md](06-risk-mechanics.md).

### Bẫy chết người nhất: Overstress dây chuyền

Nếu bất kỳ máy nào trong **cùng mạng động lực** làm mạng `overstressed`, toàn mạng dừng →
RPM của Cryo Mixer tụt từ 128 về 0 → Δ = 128 → **nổ**.

⇒ Thiết kế đúng bắt buộc:
- Cryo Mixer chạy trên **mạng động lực riêng**, có Steam Engine dự phòng riêng;
- Đặt `ta:emergency_vent_valve` cạnh buồng trộn (xả sạch chất lỏng khi nhận redstone) và
  nối nó với một Stressometer qua Redstone Link — mất áp là xả trước khi nổ;
- Dùng Clutch để cách ly mạng trước khi đổi cấu hình bánh răng.

---

## 4.3. Động năng học — Lắp ráp động cơ

### Yêu cầu

```
Sequenced Assembly: ta:rocket_engine
  ĐIỀU KIỆN: mọi Deployer / Press / Saw trong dây chuyền phải |RPM| ≥ 250
             (thực tế: đặt Rotation Speed Controller = 256 RPM — trần tốc độ của Create)
  8 vòng lặp × (deploy turbine blade → press → deploy cryo valve → press)
  results: 75 % ta:rocket_engine | 25 % 2× ta:iron_slag
```

### Vì sao 256 RPM lại đắt?

Trong Create, `SU tiêu thụ = stressImpact × RPM`. Đẩy lên trần 256 RPM nghĩa là **nhân 4 lần**
chi phí so với 64 RPM thường dùng:

| Máy | Impact | @64 RPM | @256 RPM |
|---|---:|---:|---:|
| Mechanical Press | 8 | 512 SU | 2 048 SU |
| Deployer | 4 | 256 SU | 1 024 SU |
| Reinforced Mechanical Crafter | 16 | 1 024 SU | **4 096 SU** |
| Mảng crafter 15×15 (225 máy) | — | 230 400 SU | **921 600 SU** |

Một Steam Engine ở nồi hơi tối đa cấp ≈ **16 384 SU** (1024 su/RPM × 16 RPM — kiểm tra lại theo
config Create của bạn). ⇒ riêng mảng crafter đã cần **≈ 57 Steam Engine ≈ 3–4 nồi hơi 9×9×9 max**.

### Mẹo thiết kế mà mod muốn dạy

1. **Gear up tại chỗ tiêu thụ, không gear up toàn mạng.** Dùng Rotation Speed Controller riêng
   cho từng cụm; cụm nào không cần 256 RPM thì để 64 RPM cho rẻ.
2. **Chia pha bằng Clutch.** Dây chuyền quặng và mảng crafter không cần chạy cùng lúc —
   một Sequenced Gearshift + Redstone Link giúp giảm ~40 % công suất đỉnh.
3. **Flywheel không giúp gì ở đây** — SU trong Create không có khái niệm "tích trữ".
   Cách duy nhất là thêm máy phát.
