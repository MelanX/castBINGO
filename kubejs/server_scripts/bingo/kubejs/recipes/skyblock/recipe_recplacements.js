// packmode: skyblock

onEvent('recipes', event => {
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
});