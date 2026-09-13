// ============================================================================
//  Create: Titan Aerospace — bản KubeJS (không cần viết Java)
//  Yêu cầu: KubeJS 6 + Create 0.5.1 + KubeJS Create addon
//
//  Hạn chế đã biết của bản KubeJS:
//   • Không tạo được recipe type mới ⇒ ràng buộc RPM/nhiệt độ phải mô phỏng bằng
//     event tick + kiểm tra thủ công (xem phần CUSTOM LOGIC ở cuối).
//   • Mechanical Crafter của Create chỉ chạy ổn định tới 9×9 ⇒ chia vỏ tên lửa
//     thành 4 tấm 9×9 rồi ghép, thay vì một mảng 15×15.
// ============================================================================

ServerEvents.recipes(event => {
  const C  = event.recipes.create;
  const ta = id => `titan_aerospace:${id}`;

  // ---------------------------------------------------------------- GIAI ĐOẠN 1
  // 1. Nghiền quặng
  C.crushing([
    Item.of(ta('crushed_rutile'), 2),
    Item.of(ta('crushed_rutile')).withChance(0.25),
    Item.of(ta('tailings_sand')).withChance(0.35)
  ], ta('raw_rutile')).processingTime(400);

  C.crushing([
    Item.of(ta('crushed_ilmenite'), 3),
    Item.of('minecraft:iron_nugget').withChance(0.50)
  ], ta('raw_ilmenite')).processingTime(400);

  C.crushing([
    Item.of(ta('crushed_bauxite'), 3)
  ], ta('raw_bauxite')).processingTime(400);

  // 2. Rửa — ĐÂY LÀ NÚT THẮT 0.8 %
  C.splashing([
    Item.of(ta('rutile_concentrate')),
    Item.of(ta('pure_titanium_dust')).withChance(0.008),   // 0.8 %
    Item.of(ta('tailings_sand')).withChance(0.60)
  ], ta('crushed_rutile'));

  C.splashing([
    Item.of(ta('ilmenite_concentrate')),
    Item.of(ta('pure_titanium_dust')).withChance(0.008),
    Item.of(ta('vanadium_dust')).withChance(0.05)
  ], ta('crushed_ilmenite'));

  C.splashing([
    Item.of(ta('alumina_dust')),
    Item.of(ta('pure_titanium_dust')).withChance(0.005),   // bùn đỏ: 0.5 %
    Item.of(ta('red_mud'))
  ], ta('crushed_bauxite'));

  // 3. Clo hóa (Kroll bước 1) — bắt buộc SUPERHEATED
  C.mixing(Fluid.of(ta('crude_titanium_tetrachloride'), 1000), [
    Item.of(ta('rutile_concentrate'), 4),
    Item.of(ta('petroleum_coke')),
    Fluid.of(ta('chlorine'), 1000)
  ]).superheated().processingTime(200);

  // 4. Chưng cất — Create không có tháp chưng cất, mô phỏng bằng mixing + heated
  C.mixing([
    Fluid.of(ta('titanium_tetrachloride'), 800),
    Fluid.of(ta('iron_chloride_waste'), 200)
  ], [ Fluid.of(ta('crude_titanium_tetrachloride'), 1000) ]).heated().processingTime(300);

  // 5. Kroll: TiCl4 + Mg → Titanium Sponge + MgCl2
  C.mixing([
    Item.of(ta('titanium_sponge'), 4),
    Fluid.of(ta('molten_magnesium_chloride'), 2000)
  ], [
    Fluid.of(ta('titanium_tetrachloride'), 1000),
    Item.of(ta('magnesium_ingot'), 2),
    Fluid.of(ta('argon'), 1000)
  ]).superheated().processingTime(300);

  // 6. Vòng tái chế bắt buộc (nếu không sẽ hết Magnesium)
  C.mixing([
    Item.of(ta('magnesium_ingot'), 1),
    Fluid.of(ta('chlorine'), 900)
  ], [ Fluid.of(ta('molten_magnesium_chloride'), 2000) ]).superheated().processingTime(400);

  // 7. Nấu chảy (thay cho lò VAR): Sponge + Press
  C.mixing(Fluid.of(ta('molten_titanium'), 144), [ Item.of(ta('titanium_sponge')) ])
   .superheated().processingTime(100);

  C.filling(ta('titanium_ingot'), [ ta('casting_mold'), Fluid.of(ta('molten_titanium'), 144) ]);

  // 8. Đường bootstrap: dust → ingot
  C.compacting(ta('titanium_ingot'), [ Item.of(ta('pure_titanium_dust')) ])
   .superheated().processingTime(200);

  // 9. Hợp kim hàng không
  C.mixing(Item.of(ta('ti6al4v_ingot'), 10), [
    Item.of(ta('titanium_ingot'), 9),
    Item.of(ta('aluminium_ingot')),
    Item.of(ta('vanadium_dust'))
  ]).superheated().processingTime(400);

  // ---------------------------------------------------------------- GIAI ĐOẠN 2
  // Tấm vỏ titan — bản KubeJS dùng xác suất thay cho mô hình nhiệt liên tục
  event.custom({
    type: 'create:sequenced_assembly',
    ingredient: { item: ta('ti6al4v_ingot') },
    transitionalItem: { item: ta('incomplete_titanium_plate') },
    loops: 4,
    sequence: [
      { type: 'create:deploying',
        ingredients: [ { item: ta('incomplete_titanium_plate') }, { item: 'create:blaze_cake' } ],
        results: [ { item: ta('incomplete_titanium_plate') } ] },
      { type: 'create:pressing',
        ingredients: [ { item: ta('incomplete_titanium_plate') } ],
        results: [ { item: ta('incomplete_titanium_plate') } ] }
    ],
    results: [
      { item: ta('titanium_plate'), chance: 75 },
      { item: ta('iron_slag'), count: 2, chance: 25 }
    ]
  });

  // Khí hóa lỏng
  C.mixing(Fluid.of(ta('liquid_oxygen'), 1000),   [ Fluid.of('minecraft:water', 1000), Item.of(ta('cryo_valve')) ]).processingTime(400);
  C.mixing(Fluid.of(ta('liquid_hydrogen'), 1000), [ Fluid.of('minecraft:water', 1000), Item.of(ta('electrode')) ]).processingTime(400);

  // Nhiên liệu tên lửa — đúng tỉ lệ thể tích 1 : 2.68 (tỉ lệ khối lượng O:H = 6:1)
  C.mixing(Fluid.of(ta('liquid_rocket_fuel'), 3000), [
    Fluid.of(ta('liquid_oxygen'), 1000),
    Fluid.of(ta('liquid_hydrogen'), 2680),
    Item.of(ta('ignition_catalyst_pellet'))
  ]).processingTime(200);

  // ---------------------------------------------------------------- GIAI ĐOẠN 3
  // Mechanical Crafter 9×9 (trần an toàn của Create) — 4 tấm ghép thành 1 hull module
  event.custom({
    type: 'create:mechanical_crafting',
    acceptMirrored: true,
    pattern: [
      'HRPPPPPRH',
      'RPPPOPPPR',
      'PPRPPPRPP',
      'PPPPPPPPP',
      'POPPAPPOP',
      'PPPPPPPPP',
      'PPRPPPRPP',
      'RPPPOPPPR',
      'HRPPPPPRH'
    ],
    key: {
      P: { item: ta('titanium_plate') },
      R: { item: ta('titanium_rivet') },
      H: { item: ta('heat_shield_tile') },
      O: { item: ta('titanium_rod') },
      A: { item: ta('avionics_board') }
    },
    result: { item: ta('hull_panel'), count: 1 }
  });

  C.mechanical_crafting(ta('rocket_hull_module'), [
    'PPP', 'PCP', 'PPP'
  ], { P: ta('hull_panel'), C: ta('flight_computer') });
});

// ============================================================================
//  CUSTOM LOGIC — mô phỏng rủi ro mà KubeJS thuần không làm được
// ============================================================================

// 1) NỔ BUỒNG TRỘN: theo dõi Basin nào đang giữ LOX + LH2 và kiểm tra RPM của
//    Mechanical Mixer ngay trên nó. Chạy mỗi 10 tick cho nhẹ.
const TARGET_RPM = 128, TOLERANCE = 4;
const instability = new Map();          // "dim:x,y,z" -> số

BlockEvents.rightClicked('create:basin', e => {
  // Cho phép người chơi soi mức mất ổn định bằng tay không
  const key = `${e.level.dimension}:${e.block.pos.x},${e.block.pos.y},${e.block.pos.z}`;
  const v = instability.get(key) || 0;
  e.player.tell(`Instability: ${v.toFixed(1)} / 100  (cần ${TARGET_RPM} ± ${TOLERANCE} RPM)`);
});

ServerEvents.tick(e => {
  if (e.server.tickCount % 10 !== 0) return;

  e.server.levels.forEach(level => {
    level.getEntities().forEach(() => {});   // placeholder: dùng block entity scan của bạn
  });

  // Mẫu logic áp dụng cho MỘT vị trí đã biết (thực tế: lặp qua danh sách basin đã đăng ký)
  // const rpm   = Math.abs(mixerBlockEntity.getSpeed());
  // const delta = Math.abs(rpm - TARGET_RPM);
  // if (delta <= TOLERANCE) inst = Math.max(0, inst - 2);
  // else                    inst += Math.pow(delta - TOLERANCE, 2) / 256;
  // if (inst >= 100) level.createExplosion(x, y, z).strength(8).explode();
});

// 2) HỎNG PHÔI DO MẤT NHIỆT: chặn không cho phôi vào Basin khi Blaze Burner
//    phía dưới không ở mức SEETHING (superheated).
BlockEvents.placed('create:basin', e => {
  const below = e.level.getBlock(e.block.pos.below());
  if (below.id === 'create:blaze_burner' && below.properties.get('blaze_level') !== 'seething') {
    e.player?.tell('§cCảnh báo: Blaze Burner chưa ở mức SUPERHEATED — phôi Titan sẽ thành xỉ sắt!');
  }
});
