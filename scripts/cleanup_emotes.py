import json
import os
import pathlib

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
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    emotes_path = f"{str(pathlib.Path(path).parent.absolute()) + os.path.sep}kubejs{os.path.sep}data{os.path.sep}emojiful{os.path.sep}recipes{os.path.sep}"

    for file in os.listdir(emotes_path):
        with open(emotes_path + file, "r") as f:
            data = json.loads(f.read())

        changed = fixName(data, file)

        if file == renameFile(file):
            changed = True

        if changed:
            with open(emotes_path + file, "w") as f:
                f.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
