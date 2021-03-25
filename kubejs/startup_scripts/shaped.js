events.listen('recipes', function (event) {
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

function shapedRecipe(result, pattern, key, id) {
    return {result: result, pattern: pattern, key: key, id: id};
}