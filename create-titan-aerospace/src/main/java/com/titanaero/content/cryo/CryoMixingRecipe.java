package com.titanaero.content.cryo;

import com.google.gson.JsonObject;
import com.simibubi.create.content.processing.recipe.HeatCondition;
import com.simibubi.create.content.processing.recipe.ProcessingRecipe;
import com.simibubi.create.content.processing.recipe.ProcessingRecipeBuilder.ProcessingRecipeParams;
import com.simibubi.create.foundation.fluid.FluidIngredient;
import com.titanaero.registry.TARecipeTypes;

import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.RecipeType;
import net.minecraftforge.items.wrapper.RecipeWrapper;

/**
 * Recipe type riêng cho {@code ta:cryo_mixing_chamber}.
 *
 * <p>Khác với {@code create:mixing}, recipe này mang thêm ba ràng buộc vật lý:
 * <ul>
 *   <li><b>targetRpm / tolerance</b> — tốc độ trục quay (⇒ áp suất bơm) phải nằm đúng dải,
 *       lệch ra ngoài thì {@link CryoMixerBlockEntity} tích lũy {@code instability} và phát nổ.</li>
 *   <li><b>maxTemperature</b> — nhiệt độ buồng trộn (°C). Buồng chỉ nguội được nếu còn
 *       {@code ta:liquid_nitrogen} trong két làm lạnh.</li>
 *   <li><b>coolantPerBatch</b> — lượng LN₂ tiêu hao mỗi mẻ.</li>
 * </ul>
 *
 * <p>Create gọi {@code readAdditional}/{@code writeAdditional} cho cả JSON lẫn packet,
 * nên chỉ cần override 4 hàm là recipe tự đồng bộ client ↔ server và hiện đúng trong JEI.
 */
public class CryoMixingRecipe extends ProcessingRecipe<RecipeWrapper> {

    /** Áp suất danh định (bar) tại 128 RPM — dùng để hiển thị trong JEI/tooltip. */
    public static final float BAR_PER_RPM = 40f / 128f;

    private int   targetRpm      = 128;
    private int   tolerance      = 4;
    private int   maxTemperature = -183;   // °C, điểm sôi của oxy lỏng
    private int   coolantPerBatch = 200;   // mB LN₂

    public CryoMixingRecipe(ProcessingRecipeParams params) {
        super(TARecipeTypes.CRYO_MIXING, params);
    }

    // ------------------------------------------------------------------ getters

    public int   targetRpm()       { return targetRpm; }
    public int   tolerance()       { return tolerance; }
    public int   maxTemperature()  { return maxTemperature; }
    public int   coolantPerBatch() { return coolantPerBatch; }

    public float targetPressureBar() { return targetRpm * BAR_PER_RPM; }

    /** @return true nếu {@code rpm} nằm trong dải cho phép. */
    public boolean isSpeedValid(float rpm) {
        return Math.abs(Math.abs(rpm) - targetRpm) <= tolerance;
    }

    /** @return true nếu vượt trần → nổ kiểu BLEVE; false → nổ kiểu deflagration. */
    public boolean isOverspeed(float rpm) {
        return Math.abs(rpm) > targetRpm + tolerance;
    }

    // ------------------------------------------------------- (de)serialization

    @Override
    protected void readAdditional(JsonObject json) {
        super.readAdditional(json);
        JsonObject rpm = GsonHelper.getAsJsonObject(json, "requiredRpm");
        targetRpm = GsonHelper.getAsInt(rpm, "target");
        tolerance = GsonHelper.getAsInt(rpm, "tolerance", 4);

        if (json.has("requiredTemperature")) {
            JsonObject temp = GsonHelper.getAsJsonObject(json, "requiredTemperature");
            maxTemperature = GsonHelper.getAsInt(temp, "max");
        }
        coolantPerBatch = GsonHelper.getAsInt(json, "coolantPerBatch", 200);

        if (targetRpm < 1 || targetRpm > 256)
            throw new IllegalStateException("requiredRpm.target phải trong [1, 256] — Create giới hạn 256 RPM");
        if (tolerance < 0)
            throw new IllegalStateException("requiredRpm.tolerance không được âm");
    }

    @Override
    protected void writeAdditional(JsonObject json) {
        super.writeAdditional(json);
        JsonObject rpm = new JsonObject();
        rpm.addProperty("target", targetRpm);
        rpm.addProperty("tolerance", tolerance);
        json.add("requiredRpm", rpm);

        JsonObject temp = new JsonObject();
        temp.addProperty("max", maxTemperature);
        temp.addProperty("unit", "celsius");
        json.add("requiredTemperature", temp);

        json.addProperty("coolantPerBatch", coolantPerBatch);
    }

    @Override
    protected void readAdditional(FriendlyByteBuf buffer) {
        super.readAdditional(buffer);
        targetRpm       = buffer.readVarInt();
        tolerance       = buffer.readVarInt();
        maxTemperature  = buffer.readVarInt();
        coolantPerBatch = buffer.readVarInt();
    }

    @Override
    protected void writeAdditional(FriendlyByteBuf buffer) {
        super.writeAdditional(buffer);
        buffer.writeVarInt(targetRpm);
        buffer.writeVarInt(tolerance);
        buffer.writeVarInt(maxTemperature);
        buffer.writeVarInt(coolantPerBatch);
    }

    // ----------------------------------------------------------- Create plumbing

    @Override protected int getMaxInputCount()       { return 2; }
    @Override protected int getMaxOutputCount()      { return 1; }
    @Override protected int getMaxFluidInputCount()  { return 3; }
    @Override protected int getMaxFluidOutputCount() { return 1; }

    /** Buồng trộn luôn là môi trường lạnh sâu, không bao giờ dùng HeatCondition của Create. */
    @Override
    public HeatCondition getRequiredHeat() {
        return HeatCondition.NONE;
    }

    @Override public RecipeSerializer<?> getSerializer() { return TARecipeTypes.CRYO_MIXING.getSerializer(); }
    @Override public RecipeType<?>       getType()       { return TARecipeTypes.CRYO_MIXING.getType(); }

    /** Tiện ích cho JEI: mô tả dải áp suất an toàn. */
    public String describePressureWindow() {
        return String.format("%.2f – %.2f bar @ %d ± %d RPM",
                (targetRpm - tolerance) * BAR_PER_RPM,
                (targetRpm + tolerance) * BAR_PER_RPM,
                targetRpm, tolerance);
    }

    /** Kiểm tra nhanh dùng khi datagen: fluid đầu vào có đúng tỉ lệ khối lượng 6:1 không. */
    public boolean validatesStoichiometry() {
        if (getFluidIngredients().size() < 2) return false;
        FluidIngredient lox = getFluidIngredients().get(0);
        FluidIngredient lh2 = getFluidIngredients().get(1);
        float ratio = (float) lh2.getRequiredAmount() / lox.getRequiredAmount();
        return Math.abs(ratio - 2.68f) < 0.05f;   // V_LH2 / V_LOX = 2.68
    }
}
