package com.titanaero.content.crafter;

import com.simibubi.create.content.kinetics.crafter.MechanicalCrafterBlockEntity;

/**
 * Chốt chặn tốc độ cho mảng crafter gia cường.
 *
 * <p>Gắn vào {@code ReinforcedMechanicalCrafterBlockEntity#tick()} — mảng chỉ "ăn" nguyên liệu và
 * chạy animation khi toàn bộ chuỗi crafter đều ≥ {@code minimumRpm} của recipe. Dưới ngưỡng đó
 * mảng đứng im (không phá nguyên liệu) để người chơi kịp sửa hệ truyền động.
 */
public final class ReinforcedCrafterSpeedGate {

    private ReinforcedCrafterSpeedGate() {}

    public static boolean canRun(MechanicalCrafterBlockEntity crafter, GiantMechanicalCraftingRecipe recipe) {
        float rpm = Math.abs(crafter.getSpeed());
        return rpm >= recipe.getMinimumRpm();
    }

    /**
     * Thông điệp giải thích hiện trên Goggles (Engineer's Goggles của Create).
     * Đây là cách mod "dạy" người chơi vì sao mảng không chạy, thay vì để họ đoán.
     */
    public static String goggleHint(float currentRpm, GiantMechanicalCraftingRecipe recipe) {
        if (currentRpm >= recipe.getMinimumRpm())
            return String.format("READY — %d crafters @ %.0f RPM, %,d SU",
                    recipe.getCrafterCount(), currentRpm, recipe.estimateStressCost(16));
        return String.format("TOO SLOW — cần %d RPM, đang %.0f RPM (dùng Rotation Speed Controller = 256)",
                recipe.getMinimumRpm(), currentRpm);
    }
}
