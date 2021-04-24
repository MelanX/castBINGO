onEvent('recipes', event => {
    if (!skyblockMode) {
        return
    }

    const multiSmelt = (output, input) => {
        event.smelting(output, input).xp(0.7);
        event.blasting(output, input).xp(0.7);
    };

    ingotTags = [
        'aluminum',
        'copper',
        'lead',
        'nickel',
        'silver',
        'uranium',
        'zinc'
    ];

    ingotTags.forEach(tag => {
        event.remove({output: `#forge:ingots/${tag}`, type: 'minecraft:blasting'});
        event.remove({output: `#forge:ingots/${tag}`, type: 'minecraft:smelting'});
        event.remove({output: `#forge:ingots/${tag}`, type: 'minecraft:crafting'});

        event.shapeless(`exnihilosequentia:ingot_${tag}`, [`9x #forge:nuggets/${tag}`]);
        event.shapeless(`9x exnihilosequentia:ingot_${tag}`, [`#forge:storage_blocks/${tag}`]);
        if (tag !== 'zinc') multiSmelt(`exnihilosequentia:ingot_${tag}`, `#forge:dusts/${tag}`);
        multiSmelt(`exnihilosequentia:ingot_${tag}`, `#forge:ores/${tag}`);
        multiSmelt(`exnihilosequentia:ingot_${tag}`, `create:crushed_${tag}_ore`);
    });

    recipes = [
        shapedRecipe('naturescompass:naturescompass', ['EPE', 'PMP', 'ECE'], {
            E: '#forge:gems/diamond',
            P: '#forge:ingots/gold',
            C: 'minecraft:compass',
            M: 'minecraft:heart_of_the_sea'
        })
    ];

    recipes.forEach(function (recipe) {
        if (recipe.id) {
            event.shaped(recipe.result, recipe.pattern, recipe.key).id(recipe.id);
        } else {
            event.shaped(recipe.result, recipe.pattern, recipe.key);
        }
    });
});