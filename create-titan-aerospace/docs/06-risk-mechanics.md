# 6. Cơ chế rủi ro — cài đặt chi tiết

Hai cơ chế rủi ro là "linh hồn" của mod. Nguyên tắc thiết kế chung:

> **Rủi ro phải đọc được, cảnh báo được, và phòng được bằng redstone.**
> Người chơi không bao giờ bị phạt vì "xui", mà chỉ bị phạt vì thiết kế nhà máy kém.

Vì vậy cả hai cơ chế đều:
1. Có một biến trạng thái liên tục (`integrity` / `instability`), không phải rơi xúc xắc.
2. Xuất ra **comparator signal** để làm interlock.
3. Có 3 ngưỡng cảnh báo (25 % / 50 % / 75 %) kèm âm thanh + particle khác nhau.
4. Có đường thoát hiểm (`emergency_vent_valve`, dừng nạp phôi).

---

## 6.1. NỔ BUỒNG TRỘN (Cryo Mixing Chamber)

### Biến trạng thái

| Biến | Kiểu | Ý nghĩa |
|---|---|---|
| `instability` | `float` 0 … 100 | Mức mất ổn định, lưu trong NBT |
| `target` | `int` | RPM yêu cầu, đọc từ recipe |
| `tolerance` | `int` | Dung sai, đọc từ recipe (mặc định 4) |
| `coolant` | `int` mB | LN₂ còn lại, hết → `instability` tăng thêm |

### Vòng lặp mỗi tick (chỉ khi ĐANG có mẻ)

```java
float rpm   = Math.abs(getSpeed());
float delta = Math.abs(rpm - recipe.targetRpm());

if (delta <= recipe.tolerance() && coolantTank.getFluidAmount() > 0) {
    instability = Math.max(0f, instability - 2f);       // hồi phục
    processingTicks--;                                  // tiến trình chỉ chạy khi ổn định
} else {
    float over = delta - recipe.tolerance();
    instability += (over * over) / 256f;                // BẬC HAI
    if (coolantTank.isEmpty()) instability += 1.5f;     // hết LN₂ = phạt cộng dồn
}

if (instability >= 100f) detonate();
```

### Vì sao dùng hàm bậc hai?

Sai lệch nhỏ thì gần như vô hại (có thời gian sửa), sai lệch lớn thì chết ngay — giống quan hệ
giữa áp suất và ứng suất vật liệu ngoài đời:

| RPM thực | Δ | instability/tick | Thời gian tới khi nổ |
|---:|---:|---:|---|
| 130 | 2 | 0 (trong dung sai) | — an toàn |
| 140 | 12 | 0.25 | 400 tick ≈ **20 s** |
| 148 | 20 | 1.00 | 100 tick ≈ **5 s** |
| 192 | 64 | 14.1 | 7 tick ≈ **0.35 s** |
| 0 (mạng overstressed) | 128 | 60.0 | **2 tick — gần như tức thì** |

### Hai kiểu nổ

```java
private void detonate() {
    boolean overspeed = Math.abs(getSpeed()) > recipe.targetRpm();
    int mB = inputTanks.getTotalFluidAmount();

    float power = 4.0f + Math.min(8.0f, mB / 1000f * 0.5f);   // trần 12.0
    power *= overspeed ? 1.5f : 0.75f;                        // BLEVE vs deflagration

    level.explode(null, worldPosition.getX() + .5, worldPosition.getY() + .5,
            worldPosition.getZ() + .5, power,
            overspeed,                                        // overspeed mới gây cháy
            Level.ExplosionInteraction.BLOCK);

    if (!overspeed)  freezeArea(3);   // deflagration: phủ ta:frozen_slush quanh 3 block
    inputTanks.clear();
    AllSoundEvents.STEAM.playOnServer(level, worldPosition, 2f, 0.4f);
}
```

| Kiểu | Điều kiện | Sức nổ (3000 mB) | Hiệu ứng phụ |
|---|---|---:|---|
| **BLEVE** (quá tốc) | RPM > target + tol | 8.25 | Cháy lan, phá block bán kính ~10 |
| **Deflagration** (thiếu tốc) | RPM < target − tol | 4.1 | Không cháy, phủ băng `frozen_slush`, gây `Slowness IV` |

### Cảnh báo & phòng ngừa

| `instability` | Tín hiệu |
|---:|---|
| ≥ 25 | Comparator = 4, particle `ParticleTypes.SMOKE`, âm `NOTE_BLOCK_BASS` |
| ≥ 50 | Comparator = 8, `ParticleTypes.WHITE_SMOKE`, âm `VILLAGER_NO` lặp |
| ≥ 75 | Comparator = 12, **bossbar cam** cho người chơi trong 32 block, âm `WARDEN_NEARBY_CLOSE` |
| = 100 | Nổ |

**Interlock chuẩn mà mod khuyến khích:**

```
Stressometer / Speedometer ──► Redstone Link ──► ta:emergency_vent_valve
                                              └► Clutch (ngắt mạng nạp)
```
`emergency_vent_valve` khi có redstone sẽ xả 100 % chất lỏng trong buồng (mất nguyên liệu,
nhưng không nổ) và reset `instability = 0`. Đây là "van an toàn" — mất 1 mẻ rẻ hơn mất nhà máy.

### Config

```toml
[explosions]
enabled          = true    # false → chỉ hủy mẻ, không nổ (dành cho server "hòa bình")
blockDamage      = true    # false → nổ chỉ gây sát thương entity
powerMultiplier  = 1.0
instabilityRate  = 1.0     # nhân vào (over²/256)
```

---

## 6.2. HỎNG PHÔI DO MẤT NHIỆT (Titan Forge / VAR)

### Biến trạng thái

| Biến | Ý nghĩa |
|---|---|
| `integrity` | `float` 0 … 100, bắt đầu mỗi mẻ ở 100 |
| `heatScore` | 0 … 18, tính lại mỗi 5 tick (tiết kiệm hiệu năng) |
| `insulated` | Có đủ `thermal_insulation_casing` 4 mặt không |

### Cách đọc nhiệt từ Blaze Burner của Create

```java
private int computeHeatScore() {
    int score = 0;
    for (BlockPos p : manifoldBurnerPositions) {          // 9 vị trí đã cache lúc lắp máy
        BlockState st = level.getBlockState(p);
        if (!(st.getBlock() instanceof BlazeBurnerBlock)) continue;
        HeatLevel h = st.getValue(BlazeBurnerBlock.HEAT_LEVEL);
        if (h == HeatLevel.SEETHING)      score += 2;     // Blaze Cake = "superheated"
        else if (h == HeatLevel.KINDLED)  score += 1;     // lửa thường = "heated"
    }
    return score;                                          // cần đủ 18 ⇒ cả 9 burner phải SEETHING
}
```

> `HeatLevel` là enum của Create (`com.simibubi.create.content.processing.burner.BlazeBurnerBlock.HeatLevel`):
> `NONE → SMOULDERING → FADING → KINDLED → SEETHING`. Create quy ước `KINDLED` = *heated*,
> `SEETHING` = *superheated*. Mod tái dùng đúng enum này nên tương thích 100 % với Blaze Cake,
> Blaze Burner tự động nạp bằng Deployer, và các addon khác.

### Vòng lặp mỗi tick

```java
int deficit = REQUIRED_HEAT - heatScore;          // REQUIRED_HEAT = 18
if (deficit > 0) {
    integrity -= deficit * 1.5f * (insulated ? 0.5f : 1.0f);
    spawnCoolingParticles();
} else if (integrity < 100f) {
    integrity += 0.25f;                            // hồi phục chậm gấp 6 lần tốc độ mất
}

if (integrity <= 0f) ruinWorkpiece();
```

### Xử lý khi hỏng

```java
private void ruinWorkpiece() {
    inputInv.extractItem(0, 1, false);                              // ăn mất phôi Ti-6Al-4V
    outputInv.insertItem(0, new ItemStack(TAItems.IRON_SLAG.get(), 2), false);
    integrity = 100f;  processingTicks = 0;                         // sẵn sàng cho mẻ sau
    level.playSound(null, worldPosition, SoundEvents.FIRE_EXTINGUISH,
                    SoundSource.BLOCKS, 1.2f, 0.6f);
    if (level instanceof ServerLevel sl)
        sl.sendParticles(ParticleTypes.LARGE_SMOKE,
                x + .5, y + 1.5, z + .5, 40, .5, .5, .5, .02);
    award(TAAdvancements.FIRST_SLAG);                               // advancement "Xỉ Đầu Tiên"
}
```

### Vì sao hồi phục chậm hơn mất?

Đây là lựa chọn thiết kế có chủ đích (asymmetric penalty). Nếu hồi phục nhanh bằng tốc độ mất,
người chơi sẽ "cưỡi sóng" — để nhiệt nhấp nhô quanh ngưỡng và vẫn thành công. Tỉ lệ 6:1 buộc
họ phải giữ nhiệt **ổn định tuyệt đối**, đúng tinh thần đề bài: *"nếu nguồn nhiên liệu bị ngắt
quãng làm giảm nhiệt, toàn bộ phôi sẽ bị hỏng."*

### Cách hiện thực bằng Sequenced Assembly (không cần Java)

Nếu chỉ muốn dùng datapack/KubeJS, có thể mô phỏng gần đúng bằng `create:sequenced_assembly`:
trường `results` của Create nhận danh sách kèm `chance`, nên "phôi hỏng thành xỉ" là kết quả
xác suất thay vì kết quả điều kiện:

```json
"results": [
  { "item": "titan_aerospace:titanium_plate", "chance": 75 },
  { "item": "titan_aerospace:iron_slag", "count": 2, "chance": 25 }
]
```

Nhược điểm: 25 % là **ngẫu nhiên thuần**, người chơi không thể phòng bằng thiết kế tốt hơn.
Bản Java (`TitanForgeBlockEntity`) mới đúng tinh thần "kỹ năng, không phải may rủi", nên
JSON ở trên chỉ là bản dự phòng cho modpack không muốn thêm Java.
