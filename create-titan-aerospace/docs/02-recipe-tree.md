# 2. Sơ đồ chuỗi công thức (Recipe Tree)

## 2.1. Tổng quan 3 giai đoạn

```
                    ┌──────────────── GIAI ĐOẠN 1: LUYỆN KIM ────────────────┐
  Rutile ──┐        │                                                        │
  Ilmenite ├──► Nghiền ► Ngâm axit ► Rửa/Cyclone ► Clo hóa ► Chưng cất ►    │
  Bauxite ─┘        │        │                        Kroll ► VAR ► Thỏi Ti  │
                    │        └─(0.8 %)─► Pure Titanium Dust ─► bootstrap     │
                    └────────────────────────────────────────────────────────┘
                                              │
                    ┌──────────────── GIAI ĐOẠN 2: VẬT LÝ ───────────────────┐
                    │  Ti-6Al-4V ─► Titan Forge ─► Titanium Plate            │
                    │      (nhiệt đứt = xỉ sắt)                              │
                    │  H₂O ─► Điện phân ─► H₂/O₂ ─► Hóa lỏng ─► Cryo Mixer   │
                    │      (sai RPM = NỔ)          ─► Liquid Rocket Fuel     │
                    │  Linh kiện ─► Sequenced Assembly @ 256 RPM ─► Động cơ  │
                    └────────────────────────────────────────────────────────┘
                                              │
                    ┌──────────────── GIAI ĐOẠN 3: LẮP RÁP ──────────────────┐
                    │  Crafter 15×15 ─► Hull Module ×64 ─► Multiblock 9×9×31 │
                    │  ─► Bơm 6 144 000 mB ─► T-60 ─► PHÓNG ─► END GAME      │
                    └────────────────────────────────────────────────────────┘
```

---

## 2.2. Nhánh RUTILE — dòng chính (Ti hàm lượng cao)

```
ta:rutile_ore  ──[Fortune III, Silk Touch → block]
  │
  ├─► (đào) 2× ta:raw_rutile
  │
  └─► Crushing Wheels ─────────────────────────► 2× ta:crushed_rutile (100 %)
                                                 + 1× ta:tailings_sand (35 %)
      │
      └─► ta:acid_leaching_vat
          IN : 8× crushed_rutile + 500 mB ta:sulfuric_acid   [90 RPM, 32 SU/RPM]
          OUT: 8× ta:rutile_concentrate (100 %)
               + 250 mB ta:red_mud_slurry
          │
          └─► ta:hydro_cyclone  (bước RNG duy nhất của dòng chính)
              IN : 1× rutile_concentrate + 100 mB water    [64 RPM]
              OUT: 1× rutile_concentrate (95 %)   ← trả lại, coi như "rửa sạch"
                   1× ta:pure_titanium_dust (0.8 %)  ← ĐƯỜNG BOOTSTRAP
                   1× ta:tailings_sand (60 %)
```

### Clo hóa (Kroll bước 1)

```
ta:chlorination_reactor          [64 RPM, 256 SU/RPM, HeatRequirement = SUPERHEATED]
  IN : 4× ta:rutile_concentrate
       1× ta:petroleum_coke
       1000 mB ta:chlorine
  OUT: 1000 mB ta:crude_titanium_tetrachloride
       1× ta:iron_slag (phụ phẩm)
  ⚠ Thiếu Superheated → recipe dừng (không hỏng nguyên liệu, chỉ tắc dây chuyền)
```

### Chưng cất

```
ta:distillation_column (cao ≥ 5 tầng)   [96 RPM, 96 SU/RPM mỗi tầng]
  IN : 1000 mB crude_titanium_tetrachloride
  OUT: 800 mB ta:titanium_tetrachloride
       200 mB ta:iron_chloride_waste
  ⚠ Tháp < 5 tầng → hiệu suất tụt còn 400 mB
```

### Kroll Reduction

```
ta:kroll_retort               [96 RPM, 512 SU/RPM, cần 1000 mB ta:argon/mẻ]
  IN : 1000 mB ta:titanium_tetrachloride
       2× ta:magnesium_ingot (nấu chảy tại chỗ)
       1000 mB ta:argon
  OUT: 4× ta:titanium_sponge
       2000 mB ta:molten_magnesium_chloride
  ⚠ Thiếu Argon → OUT đổi thành 4× ta:iron_slag (titan bị oxy hóa)
```

### Vòng tái chế (bắt buộc, nếu không sẽ hết Magnesium)

```
ta:electrolysis_cell           [128 RPM, 384 SU/RPM]
  IN : 2000 mB ta:molten_magnesium_chloride
  OUT: 1.8× ta:magnesium_ingot (90 %)  +  900 mB ta:chlorine (90 %)
```

### Nấu chảy cuối — Vacuum Arc Remelting

```
ta:vacuum_arc_remelter    [128 RPM, 256 SU/RPM]
  YÊU CẦU CẤU TRÚC:
    • 9× Blaze Burner ở SEETHING (Superheated, nuôi bằng Blaze Cake) dưới đáy
    • 1× Mechanical Press ngay trên nắp lò, đang chạy ≥ 64 RPM
    • 1000 mB ta:argon cho mỗi 4 mẻ
  IN : 1× ta:titanium_sponge  (100 tick / mẻ)
  OUT: 144 mB ta:molten_titanium
       │
       └─► ta:casting_table ──► 1× ta:titanium_ingot
```

---

## 2.3. Nhánh ILMENITE — nguồn Vanadium + sắt

```
ta:ilmenite_ore ─► Crushing Wheels ─► 3× ta:crushed_ilmenite
  └─► acid_leaching_vat (8× + 500 mB H₂SO₄)
      ─► 6× ta:ilmenite_concentrate + 2× minecraft:iron_nugget + 400 mB red_mud_slurry
          └─► Mixing (Superheated, Basin)
              IN : 6× ilmenite_concentrate + 1× petroleum_coke
              OUT: 4× rutile_concentrate (đưa về dòng chính)
                   1× ta:vanadium_dust (25 %)   ← nguồn V duy nhất
                   2× minecraft:iron_ingot
```

## 2.4. Nhánh BAUXITE — nguồn Aluminium

```
ta:bauxite_ore ─► Crushing Wheels ─► 3× ta:crushed_bauxite
  └─► acid_leaching_vat ─► 3× ta:alumina_dust + 1000 mB ta:red_mud_slurry
      │                                              │
      │                                              └─► hydro_cyclone
      │                                                  1× ta:pure_titanium_dust (0.5 %)
      │                                                  1× ta:red_mud (100 %)
      └─► electrolysis_cell (3× alumina_dust) ─► 2× ta:aluminium_ingot
```

## 2.5. Hợp kim hàng không

```
Mixing (Basin, HeatRequirement = SUPERHEATED, 400 tick)
  IN : 9× ta:titanium_ingot + 1× ta:aluminium_ingot + 1× ta:vanadium_dust
  OUT: 10× ta:ti6al4v_ingot           (tỉ lệ ≈ 90 / 6 / 4 như hợp kim thật)
```

---

## 2.6. GIAI ĐOẠN 2 — chi tiết

### Tấm vỏ Titan (rủi ro nhiệt)

```
ta:titan_forge  [64 RPM, 192 SU/RPM, 600 tick/mẻ, cần 9 burner SEETHING liên tục]
  IN : 1× ta:ti6al4v_ingot
  OUT (thành công, integrity > 0): 1× ta:titanium_plate
  OUT (thất bại, integrity ≤ 0) : 2× ta:iron_slag    ← "phôi hỏng thành xỉ sắt"
```

### Nhiên liệu lỏng (rủi ro RPM)

```
minecraft:water 1000 mB ─► electrolysis_cell ─► 666 mB H₂(khí) + 333 mB O₂(khí)
                                                     │
Air (Encased Fan hút) ──► ta:air_liquefier ──────────┼─► 1000 mB ta:liquid_oxygen
                                                     │   + 200 mB ta:liquid_nitrogen
                                                     └─► 1000 mB ta:liquid_hydrogen

ta:cryo_mixing_chamber      [BẮT BUỘC 128 ± 4 RPM, 128 SU/RPM, cần LN₂ làm lạnh]
  IN : 1000 mB ta:liquid_oxygen
       2680 mB ta:liquid_hydrogen        (đúng tỉ lệ khối lượng O:H = 6:1 ngoài đời)
       1× ta:ignition_catalyst_pellet
       + 200 mB ta:liquid_nitrogen (chất làm lạnh, tiêu hao)
  OUT: 3000 mB ta:liquid_rocket_fuel
  ⚠ RPM lệch → instability tăng → NỔ (xem docs/06)
```

### Động cơ (rủi ro tốc độ)

```
Sequenced Assembly @ ĐÚNG 256 RPM, 8 vòng lặp
  Base : 1× ta:combustion_chamber
  Loop : deploy ta:superalloy_turbine_blade → press → deploy ta:cryo_valve → press
  OUT  : 1× ta:rocket_engine        (75 %)
         2× ta:iron_slag            (25 %)
  ⚠ Mảng máy chạy < 250 RPM → Sequenced Assembly bỏ qua bước → phôi hỏng
```

---

## 2.7. GIAI ĐOẠN 3 — Mechanical Crafter khổng lồ

```
ta:reinforced_mechanical_crafter  mảng 15×15 = 225 máy  [250+ RPM, 16 SU/RPM mỗi máy]
  IN : 168× ta:titanium_plate
        32× ta:titanium_rivet
        16× ta:heat_shield_tile
         8× ta:titanium_rod
         1× ta:avionics_board
  OUT: 1× ta:rocket_hull_module
```

```
Tên lửa hoàn chỉnh (multi-block 9×9×31):
  64× ta:rocket_hull_module
  12× ta:cryo_fuel_tank_module
   8× ta:rocket_engine
   4× ta:avionics_bay
   1× ta:nose_cone
   1× ta:rocket_control_computer
   9× ta:launch_pad
  + 6 144 000 mB ta:liquid_rocket_fuel
  + khóa ta:launch_authorization_key
      ─────────────────────────────────► T-60 ─► PHÓNG ─► END CREDITS
```
