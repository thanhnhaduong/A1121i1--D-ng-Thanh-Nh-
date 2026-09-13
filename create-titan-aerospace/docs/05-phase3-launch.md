# 5. GIAI ĐOẠN 3 — Lắp ráp & Kết thúc trò chơi

## 5.1. Mảng Mechanical Crafter 15×15

### Vì sao phải viết recipe type riêng?

Create 0.5.1 có `create:mechanical_crafting`, nhưng serializer của nó dựa trên các helper của
`ShapedRecipe` và trong thực tế chỉ được kiểm thử tới **9×9**; ngoài ra `RecipeGridHandler`
duyệt chuỗi crafter theo đệ quy và có giới hạn an toàn. Vì vậy Titan Aerospace ship:

- recipe type riêng `titan_aerospace:giant_mechanical_crafting` (tối đa **15×15 = 225 ô**),
- một Mixin vào `RecipeGridHandler#getAllCraftersOfChainIf` để nâng trần số crafter trong chuỗi,
- block riêng `ta:reinforced_mechanical_crafter` (không trộn lẫn với crafter thường của Create,
  tránh phá vỡ cân bằng mod gốc).

Xem `src/main/java/com/titanaero/content/crafter/GiantMechanicalCraftingRecipe.java`.

### Ràng buộc vận hành

| Ràng buộc | Giá trị | Lý do |
|---|---|---|
| Kích thước mảng | đúng 15×15 (225 crafter) | Công thức `rocket_hull_module` |
| Tốc độ | ≥ 250 RPM | Ép ở 256 RPM — trần của Create |
| Stress | 16 SU/RPM × 225 × 256 = **921 600 SU** | Bắt buộc dàn Steam Engine |
| Nguồn cấp | 225 ô đầu vào ⇒ cần ~225 Belt/Funnel hoặc mạng Item Vault + Brass Tunnel | Đây là bài toán hậu cần thật sự |

> Mẹo: dùng **Item Vault + Stock Ticker/Redstone Requester** (Create 0.5.1f) hoặc một mạng
> Smart Chute + Brass Funnel với filter riêng cho từng cột để nạp đủ 225 ô.

### Công thức `ta:rocket_hull_module`

225 ô = 168 `titanium_plate` + 32 `titanium_rivet` + 16 `heat_shield_tile` + 8 `titanium_rod`
+ 1 `avionics_board`. Xem file JSON:
`src/main/resources/data/titan_aerospace/recipes/giant_crafting/rocket_hull_module.json`.

---

## 5.2. Multi-block tên lửa

### Hình dạng (9 × 9 × 31)

```
            tầng 31          ▲  ta:nose_cone (1)
         tầng 27–30          ║  ta:avionics_bay (4)
         tầng 15–26          ║  ta:cryo_fuel_tank_module (12 × 512 000 mB)
          tầng 3–14          ║  ta:rocket_hull_module (64, xếp vòng ngoài)
          tầng 1–2           ║  ta:rocket_engine (8, chụm dưới đáy)
            tầng 0           ═  ta:launch_pad 3×3 (9)  +  ta:rocket_control_computer (1)
                                ta:fuel_umbilical (1–8, gắn cạnh bệ)
```

### Thuật toán kiểm tra cấu trúc

`RocketControllerBlockEntity#validateStructure()` chạy khi người chơi right-click bằng
`ta:rocket_blueprint`, hoặc khi nhận redstone lần đầu:

1. Quét khối hộp `9×31×9` phía trên bộ điều khiển bằng `BlockPos.betweenClosedStream`.
2. Đếm từng `Block` theo bảng BOM; lệch một khối là fail.
3. Kiểm tra liên thông: mọi `rocket_hull_module` phải kề ít nhất 2 module khác (chống "vỏ thủng").
4. Nếu fail → gửi `Component.translatable("titan_aerospace.rocket.invalid", pos, expected, found)`
   vào chat và highlight ô sai bằng `CreateClient.OUTLINER.showAABB(...)` (API Create) trong 10 s.
5. Nếu pass → lưu `structureValid = true`, phát `SoundEvents.BEACON_ACTIVATE`.

### Nạp nhiên liệu

| Thông số | Giá trị |
|---|---|
| Sức chứa | 12 × 512 000 = **6 144 000 mB** |
| Tốc độ 1 `fuel_umbilical` | 256 mB/tick = 5 120 mB/s |
| Thời gian với 1 cần | 20 phút |
| Thời gian với 8 cần | **2 phút 30** |
| Yêu cầu phụ | Nhiên liệu phải là `ta:liquid_rocket_fuel`; bơm nhầm LOX/LH₂ thô → cần tự xả |

Trong lúc nạp, `rocket_control_computer` xuất comparator = `fuelLevel * 15 / capacity`
để người chơi làm bảng điều khiển bằng Nixie Tube / Display Link.

---

## 5.3. Sự kiện phóng

### Điều kiện kích hoạt

```java
canLaunch() =
      structureValid
   && fuelTank.getFluidAmount() >= 6_144_000
   && kineticInput.getSpeed() >= 128            // trục quay nạp "động năng" cho con quay hồi chuyển
   && player.getItemInHand().is(TAItems.LAUNCH_AUTHORIZATION_KEY)
   && level.dimension() == Level.OVERWORLD
```

### Chuỗi đếm ngược (T-60 → T-0), tổng 1 200 tick

| Mốc | Tick | Sự kiện |
|---|---|---|
| T-60 | 0 | Khóa cấu trúc (không phá được block), bossbar đỏ "LAUNCH SEQUENCE", tiếng còi |
| T-30 | 600 | `fuel_umbilical` tự rút (biến thành `ta:cryo_valve` rơi ra), khói LN₂ |
| T-10 | 1000 | Rung màn hình (`ClientboundSetTitleTextPacket` + camera shake của Create) |
| T-3 | 1140 | Đốt động cơ: `ParticleTypes.FLAME` + `LARGE_SMOKE` từ 8 `rocket_engine` |
| T-0 | 1200 | `launch()` |

Đếm ngược có thể **hủy** bằng cách cắt redstone trước T-10 (sau đó thì không). Nếu trong lúc đếm
ngược mà nhiên liệu bị rút hoặc cấu trúc bị phá → **Abort**: nổ cấp 8.0 tại bệ phóng.

### `launch()` — chuyển tên lửa thành Contraption của Create

Cách "đúng chuẩn Create" là mượn hệ Contraption thay vì tự viết entity render:

```java
RocketContraption contraption = new RocketContraption();
if (!contraption.assemble(level, controllerPos.above()))   // Contraption#searchMovedStructure
    return;
contraption.removeBlocksFromWorld(level, BlockPos.ZERO);

RocketEntity rocket = RocketEntity.create(level, contraption);
rocket.setPos(center.x, center.y, center.z);
level.addFreshEntity(rocket);
rocket.setThrust(0.02D);        // gia tốc, tăng dần tới 1.8 block/tick
```

`RocketEntity extends AbstractContraptionEntity` (Create) nên toàn bộ block giữ nguyên texture,
chất lỏng trong tank vẫn render, và mod không phải viết renderer mới.

### Pha bay

```
y <  120 : gia tốc 0.02 → 0.4 b/t, khói dày, âm thanh LIGHTNING_BOLT_THUNDER lặp
y 120–320: 0.4 → 1.2 b/t, tách tầng — 8 rocket_engine tách ra thành contraption con rơi xuống
y 320–1000: 1.2 → 1.8 b/t, particle END_ROD (đi vào chân không)
y > 1000 : discard() + gọi triggerEndGame()
```

### `triggerEndGame()` — màn hình kết thúc như giết Ender Dragon

```java
private void triggerEndGame(ServerLevel level, BlockPos pad) {
    ServerLevel overworld = level.getServer().overworld();
    for (ServerPlayer p : level.getServer().getPlayerList().getPlayers()) {
        TAAdvancements.REACH_ORBIT.trigger(p);                    // advancement riêng
        p.awardStat(TAStats.ROCKETS_LAUNCHED);
        // Chính cơ chế vanilla dùng khi người chơi bước vào cổng End sau khi giết Dragon:
        p.connection.send(new ClientboundGameEventPacket(
                ClientboundGameEventPacket.WIN_GAME,
                p.seenCredits ? 0.0F : 1.0F));                    // 1.0F = chạy End Poem
        p.seenCredits = true;
    }
    level.getServer().getPlayerList().broadcastSystemMessage(
            Component.translatable("titan_aerospace.launch.success")
                     .withStyle(ChatFormatting.GOLD), false);
}
```

> **Vì sao dùng `ClientboundGameEventPacket.WIN_GAME`?** Đây đúng là packet vanilla gửi khi
> người chơi đi qua cổng End sau khi hạ Ender Dragon (`ServerPlayer#changeDimension` → End Poem).
> Tham số `1.0F` bảo client phát *End Poem* rồi tới credits; `0.0F` bỏ qua poem.
> Nhờ vậy mod tái sử dụng đúng trải nghiệm "phá đảo" mà không cần screen riêng.

### Hậu phóng

- Bệ phóng để lại `ta:launch_pad` cháy sém + một `ta:flight_recorder` (kỷ vật, có NBT thời gian phóng).
- Người chơi có thể xây tên lửa thứ hai: recipe không bị khóa, chỉ có advancement là một lần.
- Server có thể bật config `titan_aerospace.endgame.credits_once_per_world = true` để chỉ chạy
  credits lần đầu (tránh spam trên server nhiều người).
