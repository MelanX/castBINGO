//priority: 1000

onEvent('server.datapack.high_priority', () => {
    const defaultConfig = {
        mode: 'normal',
        message: 'Valid modes are normal and skyblock.'
    };
    const configName = 'mode.json';
    let config = json.read(configName);
    if (!config || !config.mode) {
        json.write(configName, defaultConfig);
        console.log(`Created new ${configName}`);
    }
    if (config !== null && config.mode == 'none') {
        json.write(configName, defaultConfig);
        config.mode = defaultConfig.mode;
        console.log(
            `Overwrote ${configName}, because the mode 'none' was found. Valid modes are 'normal' and 'skyblock'.`
        );
    }
    global.packmode = config.mode;
    console.log(`Current packmode is: ${global.packmode}`);
});