package com.titanaero.content.rocket;

import java.util.HashMap;
import java.util.Map;

import com.simibubi.create.content.kinetics.base.KineticBlockEntity;

import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundGameEventPacket;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.fluids.capability.templates.FluidTank;

/**
 * "Bộ não" của tên lửa: kiểm tra cấu trúc multi-block 9×9×31, quản lý nạp nhiên liệu,
 * chạy đếm ngược T-60 và kích hoạt màn hình End Game.
 */
public class RocketControllerBlockEntity extends KineticBlockEntity {

    public  static final int FUEL_CAPACITY   = 6_144_000;   // 12 tank × 512 000 mB
    public  static final int COUNTDOWN_TICKS = 1_200;       // 60 giây
    private static final float MIN_RPM       = 128f;        // động năng nạp con quay hồi chuyển

    /** Bảng vật liệu bắt buộc của cấu trúc. */
    private static final Map<Block, Integer> BOM = new HashMap<>();
    static {
        BOM.put(TABlocks.ROCKET_HULL_MODULE.get(),     64);
        BOM.put(TABlocks.CRYO_FUEL_TANK_MODULE.get(),  12);
        BOM.put(TABlocks.ROCKET_ENGINE.get(),           8);
        BOM.put(TABlocks.AVIONICS_BAY.get(),            4);
        BOM.put(TABlocks.NOSE_CONE.get(),               1);
    }

    private final FluidTank fuelTank = new FluidTank(FUEL_CAPACITY,
            fs -> fs.getFluid().isSame(TAFluids.LIQUID_ROCKET_FUEL.get()));

    private boolean structureValid = false;
    private int     countdown      = -1;
    private boolean launched       = false;

    public RocketControllerBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
    }

    // ------------------------------------------------------------ kiểm tra cấu trúc

    /** Quét hộp 9×31×9 phía trên và so với BOM. Trả về null nếu hợp lệ, ngược lại là mô tả lỗi. */
    public Component validateStructure() {
        Map<Block, Integer> found = new HashMap<>();
        BlockPos corner = worldPosition.offset(-4, 1, -4);
        BlockPos.betweenClosedStream(corner, corner.offset(8, 30, 8))
                .forEach(p -> found.merge(level.getBlockState(p).getBlock(), 1, Integer::sum));

        for (Map.Entry<Block, Integer> e : BOM.entrySet()) {
            int have = found.getOrDefault(e.getKey(), 0);
            if (have != e.getValue()) {
                structureValid = false;
                return Component.translatable("titan_aerospace.rocket.invalid",
                        e.getKey().getName(), e.getValue(), have).withStyle(ChatFormatting.RED);
            }
        }
        structureValid = true;
        return null;
    }

    // --------------------------------------------------------------------- tick

    @Override
    public void tick() {
        super.tick();
        if (level == null || level.isClientSide || launched) return;

        if (countdown < 0) return;

        // Điều kiện phải giữ SUỐT quá trình đếm ngược — mất một cái là ABORT.
        if (!structureValid
                || fuelTank.getFluidAmount() < FUEL_CAPACITY
                || Math.abs(getSpeed()) < MIN_RPM) {
            abort();
            return;
        }

        countdown--;
        broadcastCountdown();

        if (countdown <= 0) launch();
    }

    /** Gọi khi người chơi right-click bằng {@code ta:launch_authorization_key}. */
    public boolean beginCountdown(ServerPlayer initiator) {
        Component error = validateStructure();
        if (error != null) { initiator.sendSystemMessage(error); return false; }

        if (fuelTank.getFluidAmount() < FUEL_CAPACITY) {
            initiator.sendSystemMessage(Component.translatable(
                    "titan_aerospace.rocket.low_fuel",
                    fuelTank.getFluidAmount(), FUEL_CAPACITY).withStyle(ChatFormatting.RED));
            return false;
        }
        if (Math.abs(getSpeed()) < MIN_RPM) {
            initiator.sendSystemMessage(Component.translatable(
                    "titan_aerospace.rocket.no_power", (int) MIN_RPM).withStyle(ChatFormatting.RED));
            return false;
        }

        countdown = COUNTDOWN_TICKS;
        level.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 3f, 0.5f);
        return true;
    }

    private void broadcastCountdown() {
        int t = countdown / 20;
        if (countdown % 20 != 0) return;

        if (countdown == 600) retractUmbilicals();
        if (t <= 10 || t % 10 == 0) {
            level.playSound(null, worldPosition,
                    t <= 3 ? SoundEvents.BELL_BLOCK : SoundEvents.NOTE_BLOCK_PLING.value(),
                    SoundSource.BLOCKS, 3f, t <= 3 ? 0.6f : 1.8f);
        }
        if (t <= 3 && level instanceof ServerLevel sl) igniteEngines(sl);
    }

    private void abort() {
        countdown = -1;
        level.explode(null, worldPosition.getX() + .5, worldPosition.getY() + .5, worldPosition.getZ() + .5,
                8.0f, true, Level.ExplosionInteraction.BLOCK);
        level.players().forEach(p -> p.sendSystemMessage(
                Component.translatable("titan_aerospace.rocket.abort").withStyle(ChatFormatting.DARK_RED)));
    }

    // ------------------------------------------------------------------- phóng

    private void launch() {
        if (!(level instanceof ServerLevel sl)) return;

        RocketContraption contraption = new RocketContraption();
        if (!contraption.assemble(sl, worldPosition.above())) { abort(); return; }
        contraption.removeBlocksFromWorld(sl, BlockPos.ZERO);

        RocketEntity rocket = RocketEntity.create(sl, contraption);
        rocket.setPos(worldPosition.getX() + .5, worldPosition.getY() + 1, worldPosition.getZ() + .5);
        rocket.setThrust(0.02D);                 // tăng dần tới 1.8 block/tick trong RocketEntity#tick
        sl.addFreshEntity(rocket);

        launched  = true;
        countdown = -1;
        fuelTank.setFluid(net.minecraftforge.fluids.FluidStack.EMPTY);
        sl.playSound(null, worldPosition, SoundEvents.LIGHTNING_BOLT_THUNDER, SoundSource.BLOCKS, 4f, 0.4f);
    }

    /**
     * Màn hình kết thúc — dùng đúng cơ chế vanilla khi người chơi bước vào cổng End sau khi hạ
     * Ender Dragon: packet {@code WIN_GAME}. Tham số 1.0F = phát End Poem rồi tới credits.
     *
     * <p>Được {@link RocketEntity} gọi khi tên lửa vượt y = 1000.
     */
    public static void triggerEndGame(ServerLevel level, BlockPos pad) {
        for (ServerPlayer p : level.getServer().getPlayerList().getPlayers()) {
            TAAdvancements.REACH_ORBIT.trigger(p);
            boolean seen = p.seenCredits;
            p.connection.send(new ClientboundGameEventPacket(
                    ClientboundGameEventPacket.WIN_GAME,
                    seen || TAConfig.CREDITS_ONCE_PER_WORLD.get() && level.getServer()
                            .getWorldData().isHardcore() ? 0.0F : 1.0F));
            p.seenCredits = true;
        }
        level.getServer().getPlayerList().broadcastSystemMessage(
                Component.translatable("titan_aerospace.launch.success").withStyle(ChatFormatting.GOLD),
                false);
        level.setDefaultSpawnPos(pad, 0f);   // bệ phóng thành điểm hồi sinh kỷ niệm
    }

    // ------------------------------------------------------------------- khác

    /** Comparator = mức nhiên liệu ⇒ nối Display Link ra Nixie Tube làm bảng điều khiển. */
    public int getComparatorOutput() {
        return Math.round((float) fuelTank.getFluidAmount() / FUEL_CAPACITY * 15f);
    }

    private void retractUmbilicals() { /* biến fuel_umbilical thành item rơi + hiệu ứng khói LN₂ */ }
    private void igniteEngines(ServerLevel sl) { /* particle FLAME + LARGE_SMOKE dưới 8 động cơ */ }

    @Override
    protected void write(CompoundTag tag, boolean clientPacket) {
        super.write(tag, clientPacket);
        tag.putBoolean("StructureValid", structureValid);
        tag.putBoolean("Launched", launched);
        tag.putInt("Countdown", countdown);
        tag.put("Fuel", fuelTank.writeToNBT(new CompoundTag()));
    }

    @Override
    protected void read(CompoundTag tag, boolean clientPacket) {
        super.read(tag, clientPacket);
        structureValid = tag.getBoolean("StructureValid");
        launched       = tag.getBoolean("Launched");
        countdown      = tag.getInt("Countdown");
        fuelTank.readFromNBT(tag.getCompound("Fuel"));
    }
}
