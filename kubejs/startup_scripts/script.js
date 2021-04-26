// priority: 0

onEvent('item.registry', event => {
	event.create('chunk_osmium');
	event.create('piece_osmium');
});

onEvent('block.registry', event => {
	// Register new blocks here
	// event.create('example_block').material('wood').hardness(1.0).displayName('Example Block')
});