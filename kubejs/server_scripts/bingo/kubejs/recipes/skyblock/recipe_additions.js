onEvent('recipes', event => {
    if (!skyblockMode) {
        return;
    }

    shapedRecipes = [
        shapedRecipe('minecraft:oak_sapling', ['LL', 'LL'], {
            L: 'botania:living_root'
        })
    ];

    shapelessRecipes = [
        shapelessRecipe('botania:fertilizer', ['botania:living_root'])
    ]

    event.custom(
        sieve('exnihilosequentia:dust', 'mana-and-artifice:vinteum_dust', [{
            chance: 0.15,
            mesh: 'flint'
        }]));
    event.custom(
        sieve('minecraft:sand', 'mysticalagriculture:prosperity_shard', [{
            chance: 0.03,
            mesh: 'iron'
        }, {
            chance: 0.05,
            mesh: 'diamond'
        }]));
    event.custom(
        sieve('exnihilosequentia:crushed_netherrack', 'mysticalagriculture:soul_dust', [{
            chance: 0.05,
            mesh: 'diamond'
        }]));
    event.custom(
        sieve('exnihilosequentia:crushed_netherrack', 'mysticalagriculture:soulium_dust', [{
            chance: 0.05,
            mesh: 'emerald'
        }]));
    event.custom(
        sieve('minecraft:gravel', 'powah:uraninite_raw_poor', [{
            chance: 0.03,
            mesh: 'diamond'
        }, {
            chance: 0.03,
            mesh: 'diamond'
        }]));

    shapedRecipes.forEach(function (recipe) {
        if (recipe.id) {
            event.shaped(recipe.result, recipe.pattern, recipe.key).id(recipe.id);
        } else {
            event.shaped(recipe.result, recipe.pattern, recipe.key);
        }
    });
    shapelessRecipes.forEach(function (recipe) {
        if (recipe.id) {
            event.shapeless(recipe.result, recipe.ingredients).id(recipe.id);
        } else {
            event.shapeless(recipe.result, recipe.ingredients);
        }
    });
});