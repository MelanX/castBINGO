onEvent('recipes', event => {
    recipes = [
        shapedRecipe('create:empty_blaze_burner', ['II', 'BB'], {
            I: 'create:iron_sheet',
            B: 'minecraft:iron_bars'
        }),
        shapedRecipe('create:whisk', [' A ', 'IAI', 'III'], {
            I: 'create:iron_sheet',
            A: 'create:andesite_alloy'
        }),
        shapedRecipe(item.of('create:fluid_pipe', 8), ['SIS'], {
            S: 'create:copper_sheet',
            I: '#forge:ingots/copper'
        }),
        shapedRecipe('4x minecraft:chest', ['LLL', 'L L', 'LLL'], {
            L: '#minecraft:logs'
        }),
        shapedRecipe('16x minecraft:stick', ['L', 'L'], {
            L: '#minecraft:logs'
        }),
        shapedRecipe('minecraft:hopper', ['ILI', 'ILI', ' I '], {
            I: '#forge:ingots/iron',
            L: '#minecraft:logs'
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