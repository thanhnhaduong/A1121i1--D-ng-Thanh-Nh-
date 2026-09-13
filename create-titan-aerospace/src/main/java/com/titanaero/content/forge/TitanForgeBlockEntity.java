package com.titanaero.content.forge;

import java.util.ArrayList;
import java.util.List;

import com.simibubi.create.content.kinetics.base.KineticBlockEntity;
import com.simibubi.create.content.processing.burner.BlazeBurnerBlock;
import com.simibubi.create.content.processing.burner.BlazeBurnerBlock.HeatLevel;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.items.ItemStackHandler;

/**
 * Lò rèn Titan (5×3×5).
 *
 * <p><b>Nhiệt động lực học:</b> mẻ rèn kéo dài 600 tick và chỉ thành công nếu 9 Blaze Burner bên
 * dưới giữ mức {@link HeatLevel#SEETHING} (superheated — nuôi bằng Blaze Cake) <i>suốt</i> thời
 * gian đó. Mỗi tick thiếu nhiệt làm {@code integrity} tụt; chạm 0 thì phôi Ti-6Al-4V biến thành
 * {@code ta:iron_slag}.
 *
 * <p>Tốc độ hồi phục cố ý chậm hơn tốc độ mất 6 lần, để người chơi không thể "cưỡi sóng" quanh
 * ngưỡng mà buộc phải xây kho đệm Blaze Cake + interlock.
 */
public class TitanForgeBlockEntity extends KineticBlockEntity {

    private static final int   REQUIRED_HEAT      = 18;    // 9 burner × 2 điểm (SEETHING)
    private static final int   PROCESSING_TICKS   = 600;
    private static final float DAMAGE_PER_DEFICIT = 1.5f;
    private static final float RECOVERY_PER_TICK  = 0.25f;
    private static final float MAX_INTEGRITY      = 100f;
    private static final float MIN_RPM            = 64f;

    private final ItemStackHandler input  = new ItemStackHandler(1);
    private final ItemStackHandler output = new ItemStackHandler(4);

    private final List<BlockPos> manifoldBurners = new ArrayList<>();

    private float integrity       = MAX_INTEGRITY;
    private int   processingTicks = -1;
    private int   heatScore       = 0;
    private boolean insulated     = false;

    public TitanForgeBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }

    // -------------------------------------------------------------------- tick

    @Override
    public void tick() {
        super.tick();
        if (level == null || level.isClientSide) return;

        // Cache lại vị trí burner khi mới đặt máy hoặc sau khi tải chunk.
        if (manifoldBurners.isEmpty()) scanStructure();

        if (level.getGameTime() % 5 == 0) {
            heatScore = computeHeatScore();
            insulated = checkInsulation();
        }

        if (processingTicks < 0) {
            tryStartBatch();
            regenerate();
            return;
        }

        if (Math.abs(getSpeed()) < MIN_RPM) return;      // thiếu tốc độ: mẻ đứng, KHÔNG hỏng

        int deficit = REQUIRED_HEAT - heatScore;
        if (deficit > 0) {
            integrity -= deficit * DAMAGE_PER_DEFICIT * (insulated ? 0.5f : 1.0f);
            spawnCoolingParticles(deficit);
            if (integrity <= 0f) {
                ruinWorkpiece();
                return;
            }
            return;                                      // thiếu nhiệt thì mẻ không tiến triển
        }

        regenerate();
        if (--processingTicks <= 0) finishBatch();
        setChanged();
    }

    // --------------------------------------------------------------- cấu trúc

    /**
     * Đọc mức nhiệt thật từ Blaze Burner của Create.
     * SEETHING = superheated (Blaze Cake) → 2 điểm; KINDLED = heated (lửa thường) → 1 điểm.
     */
    private int computeHeatScore() {
        int score = 0;
        for (BlockPos p : manifoldBurners) {
            BlockState st = level.getBlockState(p);
            if (!(st.getBlock() instanceof BlazeBurnerBlock)) continue;
            HeatLevel h = st.getValue(BlazeBurnerBlock.HEAT_LEVEL);
            if (h == HeatLevel.SEETHING)     score += 2;
            else if (h == HeatLevel.KINDLED) score += 1;
        }
        return score;
    }

    private void scanStructure() {
        manifoldBurners.clear();
        BlockPos base = worldPosition.below(2);
        for (int dx = -1; dx <= 1; dx++)
            for (int dz = -1; dz <= 1; dz++) {
                BlockPos p = base.offset(dx, 0, dz);
                if (level.getBlockState(p).getBlock() instanceof BlazeBurnerBlock)
                    manifoldBurners.add(p.immutable());
            }
    }

    private boolean checkInsulation() {
        int walls = 0;
        for (net.minecraft.core.Direction d : net.minecraft.core.Direction.Plane.HORIZONTAL)
            if (level.getBlockState(worldPosition.relative(d, 2))
                     .is(TABlocks.THERMAL_INSULATION_CASING.get())) walls++;
        return walls >= 4;
    }

    // --------------------------------------------------------------- mẻ rèn

    private void tryStartBatch() {
        if (input.getStackInSlot(0).isEmpty()) return;
        if (heatScore < REQUIRED_HEAT) return;           // KHÔNG cho khởi động khi chưa đủ nhiệt
        processingTicks = PROCESSING_TICKS;
        integrity       = MAX_INTEGRITY;
        sendData();
    }

    private void finishBatch() {
        input.extractItem(0, 1, false);
        output.insertItem(0, new ItemStack(TAItems.TITANIUM_PLATE.get()), false);
        processingTicks = -1;
        integrity       = MAX_INTEGRITY;
        level.playSound(null, worldPosition, SoundEvents.ANVIL_USE, SoundSource.BLOCKS, 0.6f, 1.4f);
        sendData();
    }

    /** "Phôi Titan bị hỏng và biến thành xỉ sắt." */
    private void ruinWorkpiece() {
        input.extractItem(0, 1, false);
        output.insertItem(0, new ItemStack(TAItems.IRON_SLAG.get(), 2), false);
        processingTicks = -1;
        integrity       = MAX_INTEGRITY;

        level.playSound(null, worldPosition, SoundEvents.FIRE_EXTINGUISH, SoundSource.BLOCKS, 1.2f, 0.6f);
        if (level instanceof ServerLevel sl) {
            sl.sendParticles(ParticleTypes.LARGE_SMOKE,
                    worldPosition.getX() + .5, worldPosition.getY() + 1.5, worldPosition.getZ() + .5,
                    40, .5, .5, .5, .02);
            TAAdvancements.FIRST_SLAG.trigger(sl, worldPosition);
        }
        sendData();
    }

    private void regenerate() {
        if (integrity < MAX_INTEGRITY)
            integrity = Math.min(MAX_INTEGRITY, integrity + RECOVERY_PER_TICK);
    }

    private void spawnCoolingParticles(int deficit) {
        if (!(level instanceof ServerLevel sl) || level.getGameTime() % 4 != 0) return;
        sl.sendParticles(ParticleTypes.SMOKE,
                worldPosition.getX() + .5, worldPosition.getY() + 1.2, worldPosition.getZ() + .5,
                deficit, .4, .2, .4, .01);
    }

    // ------------------------------------------------------------ giao tiếp ra

    /** Comparator = độ toàn vẹn (15 = hoàn hảo, 0 = sắp hỏng) ⇒ dùng làm interlock. */
    public int getComparatorOutput() {
        return processingTicks < 0 ? 0 : Math.max(1, Math.round(integrity / MAX_INTEGRITY * 15f));
    }

    /** Dùng cho {@code ta:thermal_probe} và Display Link. */
    public String getStatusLine() {
        if (processingTicks < 0) return "IDLE";
        return String.format("HEAT %d/%d  |  INTEGRITY %.0f%%  |  ETA %ds",
                heatScore, REQUIRED_HEAT, integrity, processingTicks / 20);
    }

    @Override
    protected void write(CompoundTag tag, boolean clientPacket) {
        super.write(tag, clientPacket);
        tag.putFloat("Integrity", integrity);
        tag.putInt("ProcessingTicks", processingTicks);
        tag.putInt("HeatScore", heatScore);
        tag.put("Input",  input.serializeNBT());
        tag.put("Output", output.serializeNBT());
    }

    @Override
    protected void read(CompoundTag tag, boolean clientPacket) {
        super.read(tag, clientPacket);
        integrity       = tag.getFloat("Integrity");
        processingTicks = tag.getInt("ProcessingTicks");
        heatScore       = tag.getInt("HeatScore");
        input.deserializeNBT(tag.getCompound("Input"));
        output.deserializeNBT(tag.getCompound("Output"));
    }
}
