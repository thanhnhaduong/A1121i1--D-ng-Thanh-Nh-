# 3. GIAI ĐOẠN 1 — Tiến trình luyện kim Titanium

## 3.1. Vì sao phải 3 loại quặng?

Mục tiêu cuối không phải titan nguyên chất mà là **Ti-6Al-4V** — hợp kim titan dùng thật trong
hàng không vũ trụ (90 % Ti, 6 % Al, 4 % V). Mỗi quặng cung cấp đúng một nguyên tố:

| Quặng | Công thức thật | Cho ra | Vai trò trong mod |
|---|---|---|---|
| **Rutile** | TiO₂ | Ti hàm lượng cao | Dòng chính, cực hiếm trong worldgen |
| **Ilmenite** | FeTiO₃ | Ti + Fe + **V** | Phổ biến, hàm lượng thấp, **nguồn Vanadium duy nhất** |
| **Bauxite** | Al₂O₃·nH₂O | **Al** + bùn đỏ (vết TiO₂) | Nguồn Aluminium + nguồn RNG phụ |

Thiếu bất kỳ quặng nào ⇒ không ra được hợp kim ⇒ không có tấm vỏ ⇒ không có tên lửa.

---

## 3.2. Hai con đường — thiết kế "bootstrap rồi công nghiệp hóa"

Đây là trục thiết kế quan trọng nhất của Giai đoạn 1:

### Đường A — BOOTSTRAP (RNG 0.5 – 1 %)

Người chơi **chưa có titan nào** nên chưa xây được nhà máy hóa chất (các multi-block đều cần
`ta:titanium_casing`). Đường duy nhất là đãi quặng thủ công-công nghiệp:

```
ta:hydro_cyclone          (40 tick / item, 64 RPM, 64 SU/RPM)
  IN : 1× *_concentrate + 100 mB water
  OUT: 0.8 % → 1× ta:pure_titanium_dust      (rutile / ilmenite)
       0.5 % → 1× ta:pure_titanium_dust      (red_mud)
       95 %  → trả lại concentrate
       60 %  → ta:tailings_sand
  ─► Compacting (Basin, SUPERHEATED): 1 dust → 1 ta:titanium_ingot
```

**Tỉ lệ 0.8 % là cố ý phi lý.** Nó tồn tại để dạy người chơi một bài học: *đừng tối ưu tỉ lệ,
hãy tối ưu throughput.* Toán cụ thể:

| Đại lượng | Giá trị |
|---|---|
| Titan cần để mở khóa nhà máy hóa chất | **256 thỏi** |
| Concentrate cần (256 / 0.008) | **32 000** |
| Ore chunk cần (≈ 1.5 concentrate / chunk) | **≈ 21 300** |
| Thời gian với 1 giàn khoan (3 chunk/s) | **≈ 2 giờ** |
| Thời gian với 4 giàn khoan + 16 cyclone | **≈ 30 phút** |

⇒ Người chơi buộc phải xây farm quặng tự động trước, không thể đào tay.

### Đường B — CÔNG NGHIỆP (Kroll Process, tất định)

Sau khi có 256 thỏi, người chơi mở khóa chuỗi Kroll. Chuỗi này **không có RNG** — đổi lại nó
ăn SU khủng khiếp và cần 5 loại multi-block nối tiếp. Đây mới là nguồn cung thật.

```
Rutile concentrate ──► Clo hóa ──► Chưng cất ──► Kroll ──► VAR ──► Thỏi
     (4 : 1000 mB)      (1250→1000)   (1000 mB→4 sponge)  (1 sponge→1 thỏi)
```

Tỉ lệ chốt: **5 rutile_concentrate → 4 titanium_ingot** (1.25 concentrate / thỏi).

---

## 3.3. Farm quặng bắt buộc: Crustal Drilling Rig

Quặng sinh trong thế giới **không đủ** (14 500 block rutile cho tên lửa = hơn 40 000 chunk).
Mod bổ sung một multi-block khoan sâu vô hạn — đây chính là "cỗ máy farm khổng lồ" mà thiết kế
yêu cầu:

```
ta:crustal_drilling_rig      7×9×7  |  1024 SU/RPM  |  min 128 RPM  ⇒ 131 072 SU / giàn
  IN : 1× ta:drill_head (hao mòn, 512 lần dùng)  +  500 mB water / mẻ
  OUT: 1× ta:raw_ore_chunk mỗi 20 tick  (3 / giây)
       └─► Crushing Wheels ─► 2 item theo trọng số:
              40 % ta:crushed_ilmenite
              25 % ta:crushed_bauxite
               8 % ta:crushed_rutile
              27 % gravel / cobbled_deepslate (rác)
```

Quy đổi: **1 raw_ore_chunk ≈ 0.56 rutile_concentrate** sau khi gộp cả nhánh ilmenite.

---

## 3.4. Bài toán cân bằng — tên lửa cần bao nhiêu?

### Bảng vật liệu (BOM) rút gọn

| Thành phần | SL | Titanium Plate | Ghi chú |
|---|---:|---:|---|
| `rocket_hull_module` | 64 | 12 800 | 168 plate + 16 heat shield (2 plate/viên) |
| `cryo_fuel_tank_module` | 12 | 2 400 | |
| `rocket_engine` | 8 (×1.33 do 75 % thành công) | 1 100 | |
| `avionics_bay` | 4 | 200 | |
| `nose_cone` | 1 | 120 | |
| `launch_pad` | 9 | 360 | |
| **Tổng plate** | | **≈ 17 000** | = 17 000 thỏi Ti-6Al-4V |

| Quy đổi | Kết quả |
|---|---|
| 17 000 Ti-6Al-4V | 15 300 Ti + 1 700 Al + 1 700 V dust |
| Rivet / rod / gear | ≈ 740 Ti |
| **Riêng tên lửa** | **≈ 16 000 thỏi Titanium** |
| Xây nhà máy (20 VAR, 225 crafter, ống, casing) | ≈ 6 000 thỏi |
| **TỔNG** | **≈ 22 000 thỏi Titanium** |

### Từ thỏi ngược về quặng

| Bước | Phép tính | Kết quả |
|---|---|---|
| Concentrate cần | 22 000 × 1.25 ÷ 0.95 | **≈ 29 000** |
| Ore chunk cần | 29 000 ÷ 0.56 | **≈ 51 700** |
| Thời gian, 1 giàn khoan | 51 700 ÷ 3 /s | 4.8 giờ |
| **Thời gian, 8 giàn khoan** | | **≈ 36 phút** |

### Số máy khuyến nghị cho throughput ~90 phút

| Máy | SL | SU mỗi cái | Tổng SU |
|---|---:|---:|---:|
| Crustal Drilling Rig | 8 | 131 072 | 1 048 576 |
| Crushing Wheels (cặp) | 24 | 1 024 | 24 576 |
| Acid Leaching Vat | 6 | 2 880 | 17 280 |
| Hydro Cyclone | 8 | 4 096 | 32 768 |
| Chlorination Reactor | 12 | 16 384 | 196 608 |
| Distillation Column (5 tầng) | 6 | 46 080 | 276 480 |
| Kroll Retort | 16 | 49 152 | 786 432 |
| Electrolysis Cell | 8 | 49 152 | 393 216 |
| Vacuum Arc Remelter | 20 | 32 768 | 655 360 |
| **Cộng dây chuyền luyện kim** | | | **≈ 3 431 000 SU** |

Chi tiết đầy đủ (kể cả Giai đoạn 2 & 3) ở [07-balance-su.md](07-balance-su.md).

---

## 3.5. Bước nung chảy — Vacuum Arc Remelter

Yêu cầu đề bài: *"Titanium chỉ có thể nung chảy bằng Superheated Blaze Burner liên tục + áp suất
lớn từ Mechanical Press."* Thiết kế:

```
        [Mechanical Press] ← trục quay ≥ 64 RPM, phải ĐANG chạy
              ▼ (nén hồ quang)
   ┌───────────────────────┐
   │  5×5×5 VAR chamber    │  ← ta:titanium_casing bao ngoài
   │  lõi: ta:cryo_casing  │  ← 1000 mB ta:argon / 4 mẻ (chống oxy hóa)
   └───────────────────────┘
        ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲ ▲
   9× Blaze Burner @ SEETHING (Blaze Cake), nối qua ta:blaze_burner_manifold
```

Điều kiện kiểm tra mỗi tick trong `VacuumArcRemelterBlockEntity#tick()`:

| Điều kiện | Thiếu thì sao |
|---|---|
| 9 burner đều ở `HeatLevel.SEETHING` | Mẻ dừng, `integrity` giảm — xem [06](06-risk-mechanics.md) |
| Mechanical Press phía trên đang chạy ≥ 64 RPM | Mẻ dừng (không hỏng) |
| Có ≥ 250 mB `ta:argon` | Output đổi thành `ta:iron_slag` (titan cháy trong không khí) |
| Tốc độ ≥ 128 RPM và đủ SU | Máy `overstressed`, toàn mạng đứng |

Thời gian: **100 tick / sponge**, ra 144 mB `ta:molten_titanium` → đổ xuống `ta:casting_table`
→ 1 `ta:titanium_ingot`.

> **Ghi chú kỹ thuật:** Create không có API "áp suất". Ở đây "áp suất" được hiện thực bằng cách
> đọc `KineticBlockEntity` của Mechanical Press ngay phía trên lò
> (`level.getBlockEntity(worldPosition.above(3)) instanceof MechanicalPressBlockEntity press
> && Math.abs(press.getSpeed()) >= 64`), cộng với việc Press phải ở trạng thái `RUNNING`.
