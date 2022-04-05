onEvent('recipes', event => {
    const idRemovals = [
        'botania:mushroom_stew',

        'create:crafting/kinetics/fluid_pipe',
        'create:crafting/kinetics/empty_blaze_burner',
        'create:crafting/kinetics/whisk',

        'cyclic:solidifier_amberalt',

        'farmersdelight:rice',

        'immersiveengineering:alloysmelter/brass',
        'immersiveengineering:metalpress/plate_brass',

        'inventorypets:biome_pet',

        'minecraft:beetroot_soup',
        'minecraft:mushroom_stew',
        'minecraft:rabbit_stew_from_brown_mushroom',
        'minecraft:rabbit_stew_from_red_mushroom',

        'naturescompass:natures_compass',
        
        'mana-and-artifice:improvised_manaweaver_wand',
        
        'feywild:fey_altar',
        'feywild:runes/alfheim_rune',
        'feywild:runes/asgard_rune',
        'feywild:runes/helheim_rune',
        'feywild:runes/joetunheim',
        'feywild:runes/midgard_rune',
        'feywild:runes/muspelheim_rune',
        'feywild:runes/nidavellir_rune',
        'feywild:runes/niflheim_rune',
        'feywild:runes/rune_air',
        'feywild:runes/rune_autumn',
        'feywild:runes/rune_earth',
        'feywild:runes/rune_envy',
        'feywild:runes/rune_fire',
        'feywild:runes/rune_gluttony',
        'feywild:runes/rune_greed',
        'feywild:runes/rune_lust',
        'feywild:runes/rune_mana',
        'feywild:runes/rune_pride',
        'feywild:runes/rune_sloth',
        'feywild:runes/rune_spring',
        'feywild:runes/rune_summer',
        'feywild:runes/rune_water',
        'feywild:runes/rune_winter',
        'feywild:runes/rune_wrath',
        'feywild:runes/vanaheim_rune'
    ];

    idRemovals.forEach((removal) => {
        event.remove({id: removal});
    });

    event.remove({type: 'xreliquary:alkahestry_crafting'});
});