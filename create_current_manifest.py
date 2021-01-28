#!/usr/bin/env python

############################################################################################################
##   _____                        _       _     _      _             ___  ___     _            __   __    ##
##  /  __ \                      (_)     | |   | |    | |            |  \/  |    | |           \ \ / /    ##
##  | /  \/ ___  _ __  _   _ _ __ _  __ _| |__ | |_   | |__  _   _   | .  . | ___| | __ _ _ __  \ V /     ##
##  | |    / _ \| '_ \| | | | '__| |/ _` | '_ \| __|  | '_ \| | | |  | |\/| |/ _ \ |/ _` | '_ \ /   \     ##
##  | \__/\ (_) | |_) | |_| | |  | | (_| | | | | |_   | |_) | |_| |  | |  | |  __/ | (_| | | | / /^\ \\   ##
##   \____/\___/| .__/ \__, |_|  |_|\__, |_| |_|\__|  |_.__/ \___/   \_|  |_/\___|_|\__,_|_| |_\/   \/    ##
##              | |     __/ |        __/ |                 __/  /                                         ##
##              |_|    |___/        |___/                 |____/                                          ##
############################################################################################################

print("#############################################")
print("#                  WARNING                  #")
print("# This only works with GD Launcher instance #")
print("#############################################")
print()

import json
import os
from datetime import datetime
import pathlib

start = datetime.now()

path = os.path.dirname(__file__)

# statics
base_path = str(pathlib.Path(path)) + os.path.sep # path to gd launcher instance
pack_version = "1.1.0"   # current pack version
author = "CastCrafter"   # modpack author
projectID = 408447       # curseforge project id
pack_name = "castBINGO!" # name displayed when imported into curseforge
mods = []                # all the mods
missing_mods = []        # all mods which are not on curseforge

if __name__ == "__main__":
    # get important information from GD Launchers config file
    with open(base_path + "config.json", "r") as f:
        data = json.loads(f.read())
        mc_version = data["modloader"][1]
        forge_version = data["modloader"][2][len(mc_version) + 1:len(data["modloader"][2])]
        for mod in data["mods"]:
            if "name" in mod:
                mods.append({
                    "_displayName": mod["name"],
                    "projectID": mod["projectID"],
                    "fileID": mod["fileID"],
                    "required": True
                })
            else:
                missing_mods.append(mod["displayName"])

    print("Successfully read config.json")
    if len(missing_mods) > 0:
        print("Following mods are missing in manifest:")
        for mod in missing_mods:
            print(mod)
        print()

    # sort mods by name
    mods = sorted(mods, key=lambda k: k["_displayName"])
    print(f"Successfully sorted all {len(mods)} mods.")

    # create current manifest
    with open(f"{base_path}manifest.json", "w") as f:
        f.write(json.dumps({
            "minecraft": {
                "version": mc_version,
                "modLoaders": [{
                    "id": f"forge-{forge_version}",
                    "primary": True
                }]
            },
            "manifestType": "minecraftModpack",
            "overrides": "overrides",
            "manifestVersion": 1,
            "version": pack_version,
            "author": author,
            "projectID": projectID,
            "name": pack_name,
            "files": mods,
            "_missingFiles": missing_mods
        }, indent=4))
    print(f"Successfully created manifest.json in {float('{:.4f}'.format((datetime.now() - start).microseconds / 1000 / 1000))} seconds")
