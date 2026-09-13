package com.titanaero.content.crafter;

import java.util.Map;

import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.titanaero.registry.TARecipeTypes;

import net.minecraft.core.NonNullList;
import net.minecraft.network.FriendlyByteBuf;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.GsonHelper;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.crafting.CraftingRecipe;
import net.minecraft.world.item.crafting.Ingredient;
import net.minecraft.world.item.crafting.RecipeSerializer;
import net.minecraft.world.item.crafting.ShapedRecipe;

/**
 * Công thức cho mảng {@code ta:reinforced_mechanical_crafter} cỡ lớn (tối đa 15×15 = 225 ô).
 *
 * <h3>Vì sao không dùng thẳng {@code create:mechanical_crafting}?</h3>
 * Serializer của Create dựa vào helper của {@link ShapedRecipe} và trong thực tế chỉ được kiểm
 * thử tới 9×9; ngoài ra {@code RecipeGridHandler} duyệt chuỗi crafter theo đệ quy với trần an
 * toàn thấp hơn 225. Titan Aerospace vì vậy ship recipe type riêng + một Mixin nâng trần, và
 * dùng block crafter riêng để không đụng tới cân bằng của Create gốc.
 *
 * <h3>Ràng buộc thêm so với Create</h3>
 * <ul>
 *   <li>{@code minimumRpm} — mảng phải quay ≥ tốc độ này (mặc định 250, thực tế đặt RSC = 256).</li>
 *   <li>{@code requiredCrafters} — số crafter trong chuỗi phải khớp chính xác width × height,
 *       chống việc người chơi "gian lận" bằng mảng nhỏ hơn.</li>
 * </ul>
 */
public class GiantMechanicalCraftingRecipe implements CraftingRecipe {

    public static final int MAX_DIMENSION = 15;

    private final ResourceLocation id;
    private final NonNullList<Ingredient> ingredients;
    private final ItemStack result;
    private final int width;
    private final int height;
    private final int minimumRpm;
    private final boolean acceptMirrored;

    public GiantMechanicalCraftingRecipe(ResourceLocation id, NonNullList<Ingredient> ingredients,
                                         ItemStack result, int width, int height,
                                         int minimumRpm, boolean acceptMirrored) {
        this.id = id;
        this.ingredients = ingredients;
        this.result = result;
        this.width = width;
        this.height = height;
        this.minimumRpm = minimumRpm;
        this.acceptMirrored = acceptMirrored;
    }

    public int  getWidth()       { return width; }
    public int  getHeight()      { return height; }
    public int  getMinimumRpm()  { return minimumRpm; }
    public int  getCrafterCount(){ return width * height; }
    public boolean acceptsMirrored() { return acceptMirrored; }

    /** SU mà cả mảng tiêu thụ ở tốc độ vận hành — dùng cho tooltip & JEI. */
    public int estimateStressCost(int impactPerCrafter) {
        return getCrafterCount() * impactPerCrafter * minimumRpm;
    }

    @Override public NonNullList<Ingredient> getIngredients() { return ingredients; }
    @Override public boolean canCraftInDimensions(int w, int h) { return w >= width && h >= height; }
    @Override public ItemStack getResultItem(net.minecraft.core.RegistryAccess access) { return result; }
    @Override public ResourceLocation getId() { return id; }
    @Override public RecipeSerializer<?> getSerializer() { return TARecipeTypes.GIANT_CRAFTING_SERIALIZER.get(); }
    @Override public net.minecraft.world.item.crafting.RecipeType<?> getType() { return TARecipeTypes.GIANT_CRAFTING_TYPE.get(); }
    @Override public boolean isSpecial() { return true; }   // không hiện trong recipe book vanilla

    @Override
    public boolean matches(net.minecraft.world.inventory.CraftingContainer container,
                           net.minecraft.world.level.Level level) {
        return matchesAt(container, false) || (acceptMirrored && matchesAt(container, true));
    }

    private boolean matchesAt(net.minecraft.world.inventory.CraftingContainer c, boolean mirrored) {
        for (int y = 0; y < height; y++)
            for (int x = 0; x < width; x++) {
                int sx = mirrored ? width - 1 - x : x;
                if (!ingredients.get(y * width + sx).test(c.getItem(y * width + x)))
                    return false;
            }
        return true;
    }

    @Override
    public ItemStack assemble(net.minecraft.world.inventory.CraftingContainer container,
                              net.minecraft.core.RegistryAccess access) {
        return result.copy();
    }

    // =====================================================================
    //  Serializer
    // =====================================================================
    public static class Serializer implements RecipeSerializer<GiantMechanicalCraftingRecipe> {

        @Override
        public GiantMechanicalCraftingRecipe fromJson(ResourceLocation id, JsonObject json) {
            Map<String, Ingredient> keys = ShapedRecipe.keyFromJson(GsonHelper.getAsJsonObject(json, "key"));
            JsonArray patternJson = GsonHelper.getAsJsonArray(json, "pattern");

            int height = patternJson.size();
            if (height == 0 || height > MAX_DIMENSION)
                throw new com.google.gson.JsonSyntaxException(
                        "pattern phải có 1.." + MAX_DIMENSION + " dòng, đang có " + height);

            String[] pattern = new String[height];
            for (int i = 0; i < height; i++) pattern[i] = GsonHelper.convertToString(patternJson.get(i), "pattern[" + i + "]");

            int width = pattern[0].length();
            if (width == 0 || width > MAX_DIMENSION)
                throw new com.google.gson.JsonSyntaxException(
                        "mỗi dòng phải dài 1.." + MAX_DIMENSION + " ký tự, đang là " + width);
            for (String row : pattern)
                if (row.length() != width)
                    throw new com.google.gson.JsonSyntaxException("mọi dòng trong pattern phải dài bằng nhau");

            NonNullList<Ingredient> ingredients = NonNullList.withSize(width * height, Ingredient.EMPTY);
            for (int y = 0; y < height; y++)
                for (int x = 0; x < width; x++) {
                    char c = pattern[y].charAt(x);
                    if (c == ' ') continue;
                    Ingredient ing = keys.get(String.valueOf(c));
                    if (ing == null)
                        throw new com.google.gson.JsonSyntaxException("ký tự '" + c + "' chưa khai báo trong key");
                    ingredients.set(y * width + x, ing);
                }

            ItemStack result = ShapedRecipe.itemStackFromJson(GsonHelper.getAsJsonObject(json, "result"));
            int minRpm = GsonHelper.getAsInt(json, "minimumRpm", 250);
            boolean mirrored = GsonHelper.getAsBoolean(json, "acceptMirrored", false);

            return new GiantMechanicalCraftingRecipe(id, ingredients, result, width, height, minRpm, mirrored);
        }

        @Override
        public GiantMechanicalCraftingRecipe fromNetwork(ResourceLocation id, FriendlyByteBuf buf) {
            int width = buf.readVarInt(), height = buf.readVarInt();
            NonNullList<Ingredient> ingredients = NonNullList.withSize(width * height, Ingredient.EMPTY);
            for (int i = 0; i < ingredients.size(); i++) ingredients.set(i, Ingredient.fromNetwork(buf));
            return new GiantMechanicalCraftingRecipe(id, ingredients, buf.readItem(),
                    width, height, buf.readVarInt(), buf.readBoolean());
        }

        @Override
        public void toNetwork(FriendlyByteBuf buf, GiantMechanicalCraftingRecipe recipe) {
            buf.writeVarInt(recipe.width);
            buf.writeVarInt(recipe.height);
            for (Ingredient ing : recipe.ingredients) ing.toNetwork(buf);
            buf.writeItem(recipe.result);
            buf.writeVarInt(recipe.minimumRpm);
            buf.writeBoolean(recipe.acceptMirrored);
        }
    }
}
