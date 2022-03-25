onEvent('recipes', event => {
    if (!normalMode) {
        return;
    }

    event.remove({mod: 'exnihilosequentia'})
});