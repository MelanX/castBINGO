// priority: 1005

function shapedRecipe(result, pattern, key, id) {
    return {result: result, pattern: pattern, key: key, id: id};
}

function shapelessRecipe(result, ingredients, id) {
    return {result: result, ingredients: ingredients, id: id};
}