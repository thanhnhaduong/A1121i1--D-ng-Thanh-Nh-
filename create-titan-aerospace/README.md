# Create: Titan Aerospace

> Addon "endgame" cho **Create Mod** theo phong cách **GregTech**: người chơi phải luyện Titanium
> bằng quy trình hóa học thật (Kroll Process), chế tạo linh kiện tên lửa dưới các ràng buộc vật lý
> (nhiệt động lực học, động lực học chất lưu, động năng học), rồi lắp ráp và phóng một tên lửa
> multi-block khổng lồ để "phá đảo" trò chơi.

| Thông số | Giá trị |
|---|---|
| Minecraft | 1.20.1 |
| Loader | Forge 47.2.x |
| Dependency | Create 0.5.1.f (`com.simibubi.create`), Flywheel, Registrate |
| Mod ID | `titan_aerospace` |
| Java | 17 |
| Thời lượng dự kiến | 40–80 giờ chơi sau khi có Steam Engine ổn định |

## Triết lý thiết kế

1. **Không có bước nào làm tay được.** Mọi công thức quan trọng đều yêu cầu máy Create
   (Crushing Wheels, Encased Fan, Basin, Mechanical Press, Mechanical Crafter) hoặc multi-block riêng.
2. **Hóa học có thật.** Chuỗi Rutile/Ilmenite/Bauxite → TiCl₄ → Kroll → Titanium Sponge → VAR
   là quy trình luyện titan ngoài đời. Hợp kim đích là **Ti-6Al-4V** (90 % Ti, 6 % Al, 4 % V) —
   đúng loại hợp kim dùng cho khung máy bay và tên lửa.
   Đây cũng là lý do mod bắt buộc **3 loại quặng**: Rutile (Ti), Ilmenite (Ti + Fe + V), Bauxite (Al).
3. **Sai là mất của.** Mất nhiệt → phôi titan thành xỉ sắt. Sai RPM → buồng trộn nổ.
   Không có "undo", chỉ có thiết kế nhà máy tốt hơn (buffer, interlock, redstone link).
4. **Quy mô là nội dung chính.** Bảng cân bằng được tính sao cho tên lửa cần
   ≈ 20 000 thỏi Titanium, ≈ 6 100 000 mB nhiên liệu lỏng và ≈ 2 000 000 SU công suất đỉnh.

## Mục lục tài liệu

| File | Nội dung |
|---|---|
| [docs/01-registry.md](docs/01-registry.md) | Danh sách đầy đủ Item / Block / Fluid mới |
| [docs/02-recipe-tree.md](docs/02-recipe-tree.md) | Sơ đồ chuỗi công thức từ quặng thô → tên lửa |
| [docs/03-phase1-titanium.md](docs/03-phase1-titanium.md) | Giai đoạn 1: luyện kim Titanium + toán cân bằng |
| [docs/04-phase2-physics.md](docs/04-phase2-physics.md) | Giai đoạn 2: 3 định luật vật lý áp dụng vào gameplay |
| [docs/05-phase3-launch.md](docs/05-phase3-launch.md) | Giai đoạn 3: lắp ráp multi-block & sự kiện phóng |
| [docs/06-risk-mechanics.md](docs/06-risk-mechanics.md) | Cơ chế rủi ro: nổ buồng trộn, hỏng phôi nhiệt |
| [docs/07-balance-su.md](docs/07-balance-su.md) | Bảng Stress Units, throughput, số Steam Engine cần |

## Code mẫu

| File | Vai trò |
|---|---|
| `src/main/java/com/titanaero/content/cryo/CryoMixingRecipe.java` | Recipe type có RPM + nhiệt độ |
| `src/main/java/com/titanaero/content/cryo/CryoMixerBlockEntity.java` | Logic mất ổn định → phát nổ |
| `src/main/java/com/titanaero/content/forge/TitanForgeBlockEntity.java` | Logic toàn vẹn nhiệt → xỉ sắt |
| `src/main/java/com/titanaero/content/crafter/GiantMechanicalCraftingRecipe.java` | Mechanical Crafter 15×15 |
| `src/main/java/com/titanaero/content/rocket/RocketControllerBlockEntity.java` | Đếm ngược, bay lên, End Game |
| `src/main/resources/data/titan_aerospace/recipes/**` | Công thức JSON (datapack) |
| `kubejs/server_scripts/titan_aerospace.js` | Bản KubeJS cho ai không muốn viết Java |

## Cấu trúc tiến trình (TL;DR)

```
Steam Engine ổn định (~32k SU)
   └─► Giai đoạn 1a: BOOTSTRAP  — rửa quặng, 0.8 % ra Pure Titanium Dust
          └─► 256 thỏi Ti đầu tiên → xây 3 multi-block hóa chất
                 └─► Giai đoạn 1b: CÔNG NGHIỆP — Kroll Process, sản lượng ổn định
                        └─► Giai đoạn 2: rèn vỏ / trộn nhiên liệu / lắp động cơ (rủi ro cao)
                               └─► Giai đoạn 3: Mechanical Crafter 15×15 → multi-block 9×9×31
                                      └─► Bơm 6.1 M mB nhiên liệu → T-minus 60 → END GAME
```
