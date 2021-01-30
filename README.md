![Logo](https://i.imgur.com/8dZAHyI.png)

[![CurseForge](http://cf.way2muchnoise.eu/full_408447_downloads.svg)](https://www.curseforge.com/minecraft/modpacks/castbingo)
[![Bugs label](https://img.shields.io/github/issues/MelanX/castBINGO/bug)](https://github.com/MelanX/castBINGO/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
[![GitHub license](https://img.shields.io/github/license/MelanX/castBINGO.svg)](https://github.com/MelanX/castBINGO/blob/dev/LICENSE)
[![GitHub release](https://img.shields.io/github/release/MelanX/castBINGO.svg)](https://GitHub.com/MelanX/castBINGO/releases/)
[![CastCrafter Server](https://img.shields.io/discord/133198459531558912.svg?color=7289da&label=CastCrafter%20Server&logo=discord&style=flat-square)](https://discord.gg/castcrafter)

### This modpack puts your knowledge to the test!

This is the official repository of the Minecraft modpack `castBINGO!` on [CurseForge](https://www.curseforge.com/minecraft/modpacks/castbingo)!
It contains all necessary files to create a server and to create a client .zip file for importing into any known launcher which can import the default CurseForge modpack files.

Releases for server and client files can be found [here](https://github.com/MelanX/castBINGO/releases).

## Dev branch

The dev branch is what it's called - a branch for the development. Any pull request should base on the dev branch.
Here are the updates for the next version. It the `manifest.json` is always up-to-date. Each mod update, downgrade, addition or removal will be pushed when it happened.

## Content
### Basic

The included content in the folders are only the files which were changed. If a config isn't changed, it don't need to be here. It will be automatically generated on first launch of the modpack.

### Server Data

The serverdata is custom for the official Bingo Events on [Twitch](https://www.twitch.tv/castcrafter).

### Script Overview

To use the scripts you need to add your tokens in `tokens.json`. The file should look
like [tokens-example.json](tokens-example.json). The twitch token needs no specific access (It only needs to be able to
convert user-names to ids). The GitHub Token needs the scopes `public_repo`, `repo:status` and `repo_deployment` and
needs push access to this repository.

**All the scripts must be run with the repository root as current working directory**

| script | description |
| :---: | :---  |
| create_current_manifest.py | Creates the manifest from GDLauncher files |
| update_emotes.py | Updates emote data for the emojiful mod based on [emotes.json](emotes.json). The generated file can be found in `build/overrides` |
| create_release.py | Creates a new release and publishes it on github. **IMPORTANT: Make sure to push your current branch before calling this!!!** |
| modlist.py | Generates the manifest from the manifest without file ids at [pack.json](pack.json) and the files in the `mods` folder. Uses a cache file `modcache.json`. THis file should be committed. |

## Contribution

You want to contribute to the project? The simplest way is to open issues if there is any. If there is a bug, use [this template](https://github.com/MelanX/castBINGO/issues/new?labels=bug&template=bug_report.md). If you only like to suggest a mod or another cool feature, use [this template](https://github.com/MelanX/castBINGO/issues/new?labels=enhancement&template=feature_request.md).

If you already created a Bingo and want to share it with the community, please make sure that it works with all the mods and configs in the [latest released version](https://github.com/MelanX/castBINGO/releases).
If everything works, you can create a [pull request](https://github.com/MelanX/castBINGO/pulls). You don't know how to create a proper bingo? [Here](https://github.com/noeppi-noeppi/Bongo/blob/master/custom-bingos.md) you can find the full documentation to the Bongo mod.

[![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg)](https://GitHub.com/MelanX/castBINGO)
