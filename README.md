# castBINGO

Melan, please add a good readme here.

## Script Overview

To use the scripts you need to add your tokens in `tokens.json`. The file should look like [tokens-example.json](tokens-example.json). The twitch token needs no specific access (It only needs to be able to convert user-names to ids). The GitHub Token needs the scopes `public_repo`, `repo:status` and `repo_deployment` and needs push access to this repository.

**All the scripts must be run with the repository root as current woring directory**

| script | description |
| :---: | :---  |
| create_current_manifest.py | Creates the manifest from GDLauncher files |
| update_emotes.py | Updates emote data for the emojiful mod based on [emotes.json](emotes.json). The generated file can be found in `build/overrides` |
| create_release.py | Creates a new release and publishes it on github. **IMPORTANT: Make sure to push your current branch before calling this!!!** |
| modlist.py | Generates the manifest from the manifest without file ids at [pack.json](pack.json) and the files in the `mods` folder. Uses a cache file `modcache.json`. THis file should be committed. |