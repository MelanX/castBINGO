#!/usr/bin/env python

import json
import os
import sys
from datetime import datetime

print("#############################################")
print("#                  WARNING                  #")
print("# This only works with GD Launcher instance #")
print("#############################################")
print()


def main():
    # statics
    if len(sys.argv) != 2:
        print("Please specify destination path as argument")
        sys.exit(1)

    base_path = sys.argv[1]    # path to gd launcher instance
    pack_version = "1.1.0"     # current pack version
    author = "CastCrafter"     # modpack author
    projectID = 408447         # curseforge project id
    pack_name = "castBINGO!"   # name displayed when imported into curseforge
    mods = []                  # all the mods
    missing_mods = []          # all mods which are not on curseforge

    # get important information from GD Launchers config file
    with open(base_path + os.path.sep + "config.json", mode="r") as f:
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
    with open(f"{base_path + os.path.sep}manifest.json", mode="w") as f:
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


if __name__ == "__main__":
    start = datetime.now()
    main()
    print(f"Successfully created manifest.json in {float('{:.4f}'.format((datetime.now() - start).microseconds / 1000 / 1000))} seconds")