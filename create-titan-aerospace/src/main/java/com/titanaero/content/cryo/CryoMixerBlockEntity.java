package com.titanaero.content.cryo;

import java.util.List;
import java.util.Optional;

import com.simibubi.create.AllSoundEvents;
import com.simibubi.create.content.kinetics.base.KineticBlockEntity;
import com.simibubi.create.foundation.blockEntity.behaviour.BlockEntityBehaviour;
import com.simibubi.create.foundation.fluid.SmartFluidTank;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraftforge.fluids.FluidStack;

/**
 * Buồng trộn siêu lạnh — nơi Oxy lỏng + Hydro lỏng thành Liquid Rocket Fuel.
 *
 * <p><b>Cơ chế rủi ro:</b> mẻ chỉ tiến triển khi RPM nằm trong dải của recipe. Lệch dải thì
 * {@code instability} tăng theo hàm <i>bậc hai</i> của độ lệch; chạm 100 là nổ. Cách duy nhất
 * để cứu là xả buồng (ta:emergency_vent_valve) hoặc kéo RPM về dải kịp thời.
 *
 * <p>Toàn bộ hằng số ở đây nhân với hệ số config để server tự cân bằng lại được.
 */
public class CryoMixerBlockEntity extends KineticBlockEntity {

    public  static final float MAX_INSTABILITY   = 100f;
    private static final float RECOVERY_PER_TICK = 2f;
    private static final float QUADRATIC_DIVISOR = 256f;
    private static final float NO_COOLANT_PENALTY = 1.5f;

    private final SmartFluidTank[] inputTanks = new SmartFluidTank[2];
    private final SmartFluidTank   outputTank;
    private final SmartFluidTank   coolantTank;      // ta:liquid_nitrogen

    private CryoMixingRecipe currentRecipe;
    private int   processingTicks = -1;
    private float instability     = 0f;
    private int   lastWarningTier = 0;

    public CryoMixerBlockEntity(BlockEntityType<?> type, BlockPos pos, BlockState state) {
        super(type, pos, state);
        inputTanks[0] = new SmartFluidTank(16_000, this::onFluidChanged);
        inputTanks[1] = new SmartFluidTank(16_000, this::onFluidChanged);
        outputTank    = new SmartFluidTank(16_000, this::onFluidChanged);
        coolantTank   = new SmartFluidTank( 8_000, this::onFluidChanged);
    }

    @Override
    public void addBehaviours(List<BlockEntityBehaviour> behaviours) {
        super.addBehaviours(behaviours);
        // FilteringBehaviour + LinkBehaviour (Redstone Link) được thêm ở đây để người chơi
        // có thể theo dõi instability từ xa và tự động kích hoạt emergency vent.
    }

    // ------------------------------------------------------------------- tick

    @Override
    public void tick() {
        super.tick();
        if (level == null || level.isClientSide) {
            if (level != null) spawnClientEffects();
            return;
        }

        if (currentRecipe == null) {
            if (level.getGameTime() % 20 == 0) tryStartBatch();
            decayInstability();
            return;
        }

        float rpm   = Math.abs(getSpeed());
        float delta = Math.abs(rpm - currentRecipe.targetRpm());

        if (rpm < 1f) {                       // mạng đứng (overstressed / mất nguồn)
            instability += 60f;               // Δ=128 ⇒ nổ gần như tức thì, đúng thiết kế
        } else if (currentRecipe.isSpeedValid(rpm) && !coolantTank.isEmpty()) {
            instability = Math.max(0f, instability - RECOVERY_PER_TICK);
            if (--processingTicks <= 0) finishBatch();
        } else {
            float over = Math.max(0f, delta - currentRecipe.tolerance());
            instability += (over * over) / QUADRATIC_DIVISOR;
            if (coolantTank.isEmpty()) instability += NO_COOLANT_PENALTY;
        }

        if (instability >= MAX_INSTABILITY) {
            detonate();
            return;
        }
        emitWarnings();
        setChanged();
    }

    // -------------------------------------------------------------- recipe flow

    private void tryStartBatch() {
        Optional<CryoMixingRecipe> match = CryoMixingRecipeFinder.find(level, inputTanks, coolantTank);
        if (match.isEmpty()) return;
        currentRecipe   = match.get();
        processingTicks = currentRecipe.getProcessingDuration();
        instability     = 0f;
        sendData();
    }

    private void finishBatch() {
        FluidStack result = currentRecipe.getFluidResults().get(0).copy();
        if (outputTank.fill(result, net.minecraftforge.fluids.capability.IFluidHandler.FluidAction.SIMULATE)
                != result.getAmount()) {
            processingTicks = 1;       // đầu ra đầy → giữ mẻ, KHÔNG hủy (không phạt oan người chơi)
            return;
        }
        currentRecipe.getFluidIngredients()
                .forEach(ing -> drainMatching(ing.getMatchingFluidStacks().get(0)));
        coolantTank.drain(currentRecipe.coolantPerBatch(),
                net.minecraftforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);
        outputTank.fill(result, net.minecraftforge.fluids.capability.IFluidHandler.FluidAction.EXECUTE);

        currentRecipe   = null;
        processingTicks = -1;
        award();
        sendData();
    }

    // ------------------------------------------------------------------- nổ

    private void detonate() {
        boolean overspeed = currentRecipe != null && currentRecipe.isOverspeed(getSpeed());
        int storedMb = inputTanks[0].getFluidAmount() + inputTanks[1].getFluidAmount()
                     + outputTank.getFluidAmount();

        float power = 4.0f + Math.min(8.0f, storedMb / 1000f * 0.5f);
        power *= overspeed ? 1.5f : 0.75f;
        power *= TAConfig.EXPLOSION_POWER_MULTIPLIER.get().floatValue();

        // Dọn sạch trước khi nổ để tránh chất lỏng "sống sót" trong block entity bị phá.
        inputTanks[0].setFluid(FluidStack.EMPTY);
        inputTanks[1].setFluid(FluidStack.EMPTY);
        outputTank.setFluid(FluidStack.EMPTY);
        currentRecipe   = null;
        processingTicks = -1;
        instability     = 0f;

        if (!TAConfig.EXPLOSIONS_ENABLED.get()) {
            level.playSound(null, worldPosition, SoundEvents.FIRE_EXTINGUISH, SoundSource.BLOCKS, 1f, 0.5f);
            return;
        }

        level.explode(null,
                worldPosition.getX() + 0.5, worldPosition.getY() + 0.5, worldPosition.getZ() + 0.5,
                power,
                overspeed,                                    // chỉ BLEVE mới gây cháy
                TAConfig.EXPLOSION_BLOCK_DAMAGE.get()
                        ? Level.ExplosionInteraction.BLOCK
                        : Level.ExplosionInteraction.NONE);

        if (!overspeed) freezeArea(3);                        // deflagration lạnh
        AllSoundEvents.STEAM.playOnServer(level, worldPosition, 2f, 0.4f);
    }

    /** Deflagration để lại vùng băng — nguy hiểm cho người chơi nhưng không phá nhà máy. */
    private void freezeArea(int radius) {
        BlockPos.betweenClosedStream(worldPosition.offset(-radius, -1, -radius),
                                     worldPosition.offset(radius, radius, radius))
                .filter(p -> level.getBlockState(p).isAir() && !level.getBlockState(p.below()).isAir())
                .forEach(p -> level.setBlockAndUpdate(p.immutable(),
                        TABlocks.FROZEN_SLUSH.getDefaultState()));
    }

    // -------------------------------------------------------------- cảnh báo

    private void emitWarnings() {
        int tier = (int) (instability / 25f);      // 0..4
        if (tier == lastWarningTier) return;
        lastWarningTier = tier;
        if (tier <= 0 || !(level instanceof ServerLevel sl)) return;

        switch (tier) {
            case 1 -> {
                sl.sendParticles(ParticleTypes.SMOKE, cx(), cy(), cz(), 10, .3, .3, .3, .01);
                sl.playSound(null, worldPosition, SoundEvents.NOTE_BLOCK_BASS.value(),
                        SoundSource.BLOCKS, 1f, 0.5f);
            }
            case 2 -> {
                sl.sendParticles(ParticleTypes.WHITE_SMOKE, cx(), cy(), cz(), 30, .5, .5, .5, .03);
                sl.playSound(null, worldPosition, SoundEvents.VILLAGER_NO, SoundSource.BLOCKS, 1f, 0.7f);
            }
            default -> {
                sl.playSound(null, worldPosition, SoundEvents.WARDEN_NEARBY_CLOSEST,
                        SoundSource.BLOCKS, 2f, 1f);
                for (Player p : sl.getEntitiesOfClass(Player.class,
                        new net.minecraft.world.phys.AABB(worldPosition).inflate(32)))
                    p.displayClientMessage(
                            Component.translatable("titan_aerospace.mixer.critical",
                                    (int) instability), true);
            }
        }
    }

    /** Comparator đọc mức mất ổn định ⇒ người chơi làm interlock bằng redstone. */
    public int getComparatorOutput() {
        return Math.round(instability / MAX_INSTABILITY * 15f);
    }

    /** Gọi từ {@code ta:emergency_vent_valve}: xả sạch, mất nguyên liệu nhưng không nổ. */
    public void emergencyVent() {
        inputTanks[0].setFluid(FluidStack.EMPTY);
        inputTanks[1].setFluid(FluidStack.EMPTY);
        currentRecipe   = null;
        processingTicks = -1;
        instability     = 0f;
        lastWarningTier = 0;
        if (level != null)
            level.playSound(null, worldPosition, SoundEvents.LAVA_EXTINGUISH, SoundSource.BLOCKS, 1.5f, 1.4f);
        sendData();
    }

    private void decayInstability() {
        if (instability > 0f) instability = Math.max(0f, instability - RECOVERY_PER_TICK);
    }

    // -------------------------------------------------------------------- NBT

    @Override
    protected void write(CompoundTag tag, boolean clientPacket) {
        super.write(tag, clientPacket);
        tag.putFloat("Instability", instability);
        tag.putInt("ProcessingTicks", processingTicks);
        tag.put("InputA",  inputTanks[0].writeToNBT(new CompoundTag()));
        tag.put("InputB",  inputTanks[1].writeToNBT(new CompoundTag()));
        tag.put("Output",  outputTank.writeToNBT(new CompoundTag()));
        tag.put("Coolant", coolantTank.writeToNBT(new CompoundTag()));
    }

    @Override
    protected void read(CompoundTag tag, boolean clientPacket) {
        super.read(tag, clientPacket);
        instability     = tag.getFloat("Instability");
        processingTicks = tag.getInt("ProcessingTicks");
        inputTanks[0].readFromNBT(tag.getCompound("InputA"));
        inputTanks[1].readFromNBT(tag.getCompound("InputB"));
        outputTank.readFromNBT(tag.getCompound("Output"));
        coolantTank.readFromNBT(tag.getCompound("Coolant"));
    }

    private double cx() { return worldPosition.getX() + 0.5; }
    private double cy() { return worldPosition.getY() + 1.2; }
    private double cz() { return worldPosition.getZ() + 0.5; }

    private void onFluidChanged() { setChanged(); sendData(); }
    private void drainMatching(FluidStack stack) { /* rút đúng tank chứa fluid tương ứng */ }
    private void award() { /* trigger advancement titan_aerospace:first_fuel */ }
    private void spawnClientEffects() { /* sương LN₂ + rung khi instability cao */ }
}
