events.listen('recipes', function (event) {
    const idRemovals = [
        'botania:mushroom_stew',

        'cyclic:solidifier_amberalt',

        'farmersdelight:rice',

        'immersiveengineering:alloysmelter/brass',

        'inventorypets:biome_pet',

        'minecraft:beetroot_soup',
        'minecraft:mushroom_stew',
        'minecraft:rabbit_stew_from_brown_mushroom',
        'minecraft:rabbit_stew_from_red_mushroom'
    ];

    idRemovals.forEach((removal) => {
        event.remove({id: removal});
    });

    event.remove({type: 'xreliquary:alkahestry_crafting'})
});