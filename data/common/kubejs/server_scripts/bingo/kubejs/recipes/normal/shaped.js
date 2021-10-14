// packmode: normal

onEvent('recipes', event => {
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