#!/usr/bin/env python3

import json
import os
import sys

prefixes = ["te_", "pu_"]


def fixName(data: dict, file: str):
    for prefix in prefixes:
        if data["name"].startswith(prefix):
            print(f"Fix name of {file}...")
            data["name"] = data["name"].replace(prefix, "", 1)
            return True


def renameFile(file: str):
    for prefix in prefixes:
        if file.startswith(prefix):
            print(f"Rename \"{file}\" to \"{file.replace(prefix, '', 1)}...")
            file = file.replace(prefix, "", 1)
            return file


def main():
    if len(sys.argv) != 2:
        print("Please specify destination path as argument")
        sys.exit(1)

    emotes_path = sys.argv[1]

    for file in os.listdir(emotes_path):
        with open(emotes_path + os.path.sep + file, mode="r") as f:
            data = json.loads(f.read())

        changed = fixName(data, file)

        if file == renameFile(file):
            changed = True

        if changed:
            with open(emotes_path + os.path.sep + file, mode="w") as f:
                f.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
