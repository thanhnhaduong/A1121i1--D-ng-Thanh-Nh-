# 1. Danh sách Item / Block / Fluid mới

Namespace: `titan_aerospace:` (viết tắt `ta:` trong bảng dưới).

---

## 1.1. FLUIDS (12 chất lỏng)

| ID | Tên hiển thị | Nhiệt độ (°C) | Vai trò | Ghi chú kỹ thuật |
|---|---|---|---|---|
| `ta:chlorine` | Khí Clo | 25 | Dung môi clo hóa quặng | `density = -2`, `isGaseous = true` → trôi lên trong pipe |
| `ta:crude_titanium_tetrachloride` | TiCl₄ Thô | 140 | Sản phẩm clo hóa, lẫn FeCl₃ | Phải chưng cất |
| `ta:titanium_tetrachloride` | TiCl₄ Tinh Khiết | 140 | Nguyên liệu Kroll | |
| `ta:iron_chloride_waste` | Nước Thải FeCl₃ | 90 | Phế phẩm | Gây `Poison II` khi bơi vào |
| `ta:molten_magnesium` | Magnesium Nóng Chảy | 700 | Chất khử trong Kroll | |
| `ta:molten_magnesium_chloride` | MgCl₂ Nóng Chảy | 750 | Phế phẩm Kroll | Điện phân → tái sinh Mg + Cl₂ (90 %) |
| `ta:argon` | Khí Argon | 25 | Khí trơ bảo vệ lò Kroll & VAR | Thiếu Argon → mẻ titan bị oxy hóa |
| `ta:sulfuric_acid` | Axit Sulfuric | 25 | Ngâm rửa quặng, tách bùn đỏ | Ăn mòn: phá hủy Copper/Iron Pipe, bắt buộc dùng `ta:titanium_pipe` |
| `ta:red_mud_slurry` | Bùn Đỏ | 60 | Phế phẩm bauxite, chứa vết TiO₂ | Nguồn RNG phụ |
| `ta:molten_titanium` | Titanium Nóng Chảy | 1668 | Ra từ lò VAR | Đốt cháy entity, phá block gỗ khi tràn |
| `ta:liquid_oxygen` | Oxy Lỏng (LOX) | −183 | Oxidizer | Cần `ta:cryo_pipe`; pipe thường → vỡ |
| `ta:liquid_hydrogen` | Hydro Lỏng (LH₂) | −253 | Fuel | Rò rỉ + lửa = nổ |
| `ta:liquid_rocket_fuel` | Nhiên Liệu Tên Lửa | −200 | Sản phẩm cuối của Giai đoạn 2 | Đơn vị nạp vào tên lửa |
| `ta:liquid_nitrogen` | Nitơ Lỏng | −196 | Chất làm lạnh cho Cryo Mixer | Không đủ LN₂ → nhiệt độ tăng → hỏng mẻ |

*(13 mục — `ta:crude_titanium_tetrachloride` và `ta:titanium_tetrachloride` tính là 2 fluid riêng để bắt buộc bước chưng cất.)*

---

## 1.2. BLOCKS

### a) Quặng & khối lưu trữ

| ID | Sinh ra ở | Ghi chú worldgen |
|---|---|---|
| `ta:rutile_ore` / `ta:deepslate_rutile_ore` | y = −40 … 20, vein 3–5 block, 1 vein / 12 chunk | Quặng Ti hàm lượng cao, cực hiếm |
| `ta:ilmenite_ore` / `ta:deepslate_ilmenite_ore` | y = −64 … 0, vein 8–14 block, 1 vein / 4 chunk | Phổ biến hơn, hàm lượng thấp, kèm Fe + V |
| `ta:bauxite_ore` | y = 40 … 80, chỉ ở Badlands / Desert / Savanna | Nguồn Aluminium |
| `ta:titanium_block`, `ta:ti6al4v_block`, `ta:aluminium_block`, `ta:magnesium_block` | — | Khối lưu trữ 9 thỏi |
| `ta:titanium_sponge_block` | — | Nén 9 Titanium Sponge, dùng nạp lò VAR |

### b) Vật liệu xây dựng & đường ống

| ID | Chức năng |
|---|---|
| `ta:titanium_casing` | Casing chuẩn Create cho toàn bộ máy của mod |
| `ta:thermal_insulation_casing` | Bắt buộc bao quanh lò rèn, giảm 50 % tốc độ mất nhiệt |
| `ta:cryo_casing` | Bắt buộc bao quanh Cryo Mixer, giữ LN₂ |
| `ta:titanium_pipe` | Ống chịu axit (thay Fluid Pipe khi tải `sulfuric_acid`, `molten_*`) |
| `ta:cryo_pipe` | Ống chân không 2 lớp, bắt buộc cho LOX / LH₂ / LN₂ |
| `ta:blaze_burner_manifold` | Ống góp nhiệt: gom 9 Blaze Burner, báo cáo `HeatLevel` thấp nhất cho multi-block |
| `ta:rocket_scaffold` | Giàn giáo lắp ráp, đánh dấu vùng hợp lệ của tên lửa |

### c) Máy móc / Multi-block

| ID | Kích thước | SU/RPM | RPM tối thiểu | Chức năng |
|---|---|---|---|---|
| `ta:acid_leaching_vat` | 3×2×3 | 32 | 32 | Ngâm quặng nghiền trong H₂SO₄ → tinh quặng + bùn đỏ |
| `ta:hydro_cyclone` | 1×3×1 | 64 | 64 | Rửa/phân loại theo tỉ trọng — nguồn RNG `pure_titanium_dust` |
| `ta:chlorination_reactor` | 3×3×3 | 256 | 64 | Tinh quặng + Coke + Cl₂ → TiCl₄ thô. **Cần Superheated** |
| `ta:distillation_column` | 3×(5..9)×3 | 96 / tầng | 96 | Tách FeCl₃ khỏi TiCl₄ |
| `ta:kroll_retort` | 5×5×5 | 512 | 96 | TiCl₄ + Mg lỏng + Argon → Titanium Sponge + MgCl₂ |
| `ta:electrolysis_cell` | 3×3×3 | 384 | 128 | H₂O → H₂ + O₂; MgCl₂ → Mg + Cl₂ (vòng tái chế) |
| `ta:vacuum_arc_remelter` | 5×5×5 | 256 | 128 | Sponge → Molten Titanium. **9 Superheated Burner + Mechanical Press ở đỉnh** |
| `ta:casting_table` | 1×1×1 | 0 | — | Molten Titanium 144 mB → 1 thỏi |
| `ta:air_liquefier` | 3×3×3 | 384 | 128 | Không khí → LOX + LN₂ |
| `ta:cryo_mixing_chamber` | 3×3×3 | 128 | **128 ± 4 (chính xác)** | LOX + LH₂ → Liquid Rocket Fuel. **Nổ nếu sai RPM** |
| `ta:titan_forge` | 5×3×5 | 192 | 64 | Rèn Titanium Plate. **Mất nhiệt = phôi hỏng thành xỉ** |
| `ta:reinforced_mechanical_crafter` | mảng tới 15×15 | 16 / máy | **250** | Mechanical Crafter cỡ lớn |
| `ta:emergency_vent_valve` | 1×1×1 | 0 | — | Xả khẩn cấp Cryo Mixer, cứu nhà máy khỏi nổ |

### d) Block cấu thành tên lửa (dùng trong multi-block)

| ID | Số lượng trong tên lửa | Ghi chú |
|---|---|---|
| `ta:rocket_hull_module` | 64 | Sản phẩm của Mechanical Crafter 15×15 |
| `ta:cryo_fuel_tank_module` | 12 | Mỗi module chứa 512 000 mB |
| `ta:rocket_engine` | 8 | Động cơ phản lực, lắp ở 256 RPM |
| `ta:avionics_bay` | 4 | Chứa bảng mạch điều hướng |
| `ta:nose_cone` | 1 | Đỉnh tên lửa |
| `ta:launch_pad` | 9 (3×3) | Bệ phóng, chịu nhiệt |
| `ta:rocket_control_computer` | 1 | "Bộ não": đếm ngược, kiểm tra cấu trúc, kích hoạt End Game |
| `ta:fuel_umbilical` | 1–8 | Cần tiếp nhiên liệu, 256 mB/tick mỗi cái |

---

## 1.3. ITEMS

### a) Chuỗi quặng

`ta:raw_rutile`, `ta:raw_ilmenite`, `ta:raw_bauxite`
→ `ta:crushed_rutile`, `ta:crushed_ilmenite`, `ta:crushed_bauxite`
→ `ta:rutile_concentrate`, `ta:ilmenite_concentrate`, `ta:alumina_dust`
→ phế phẩm: `ta:tailings_sand`, `ta:red_mud`, `ta:iron_slag`

### b) Vật liệu trung gian

| ID | Mô tả |
|---|---|
| `ta:pure_titanium_dust` | **Phần thưởng RNG 0.8 %** — đường bootstrap |
| `ta:titanium_sponge` | Sản phẩm quy trình Kroll |
| `ta:titanium_ingot`, `ta:titanium_nugget` | Kim loại nguyên chất |
| `ta:ti6al4v_ingot` | Hợp kim hàng không (9 Ti + 1 Al + 1 V dust → 10) |
| `ta:aluminium_ingot`, `ta:magnesium_ingot` | Kim loại phụ trợ |
| `ta:vanadium_dust` | Phụ phẩm từ `ilmenite_concentrate` |
| `ta:petroleum_coke` | Chất khử cho lò clo hóa (từ Blaze Cake + Coal Block) |
| `ta:titanium_plate` | Tấm vỏ, ra từ Titan Forge (rủi ro nhiệt) |
| `ta:titanium_rivet`, `ta:titanium_rod`, `ta:titanium_gear` | Chi tiết nhỏ, đếm bằng hàng trăm nghìn |
| `ta:heat_shield_tile` | Gạch chắn nhiệt (Titanium Plate + Blaze Cake nén) |

### c) Linh kiện tên lửa

| ID | Máy chế tạo |
|---|---|
| `ta:combustion_chamber` | Reinforced Mechanical Crafter 9×9 |
| `ta:nozzle_bell` | Titan Forge + Mechanical Press (deploy 3 lần) |
| `ta:turbopump_assembly` | Sequenced Assembly, yêu cầu 256 RPM |
| `ta:superalloy_turbine_blade` | Titan Forge |
| `ta:avionics_board` | Sequenced Assembly (Gold + Redstone + Diamond + Ti) |
| `ta:gyroscope_module` | Cần chạy đúng 256 RPM khi deploy |
| `ta:flight_computer` | Crafter 9×9, gộp 4 avionics board |
| `ta:cryo_valve` | Van chịu lạnh |

### d) Item trung gian "incomplete" (Sequenced Assembly)

`ta:incomplete_titanium_plate`, `ta:incomplete_avionics_board`,
`ta:incomplete_turbopump`, `ta:incomplete_hull_module`
→ Nếu quy trình đứt đoạn, chúng rơi ra thế giới và **không thể craft tiếp** (phải nấu lại thành xỉ).

### e) Item đặc biệt

| ID | Chức năng |
|---|---|
| `ta:rocket_blueprint` | Sách hướng dẫn + kiểm tra cấu trúc (shift + right click lên `rocket_control_computer` để soi lỗi lắp) |
| `ta:launch_authorization_key` | Chìa khóa phóng, craft từ 1 `flight_computer` + 1 Nether Star |
| `ta:thermal_probe` | Cầm tay, chỉ ra nhiệt độ/độ toàn vẹn của mẻ đang rèn |
| `ta:pressure_gauge` | Hiển thị RPM yêu cầu vs RPM hiện tại của Cryo Mixer |
