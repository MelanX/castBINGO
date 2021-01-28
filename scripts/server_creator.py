import json
import sys
import tempfile
from urllib.request import urlopen, Request
import subprocess
import shutil
import os
import pathlib

branch = "dev"

copy_paths = [
    "config",
    "defaultconfigs",
    "kubejs"
]


def main():
    # Hey, __path__ ist suboptimal, da nicht zuverlässig. Offiziell wäre sys.argv[0] damit das von bat / sh funktioniert
    path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    base_path = str(pathlib.Path(path).parent.absolute()) + os.path.sep # path to gd launcher instance

    print(base_path)

    version_checker_url = "https://raw.githubusercontent.com/MelanX/castBINGO/dev/changelogs/updates.json"
    version = json.loads(urlopen(Request(version_checker_url)).read())["latest"]

    if len(sys.argv) != 2:
        print('Please specify destination path as argument')
        sys.exit(1)

    if os.path.isdir(sys.argv[1]):
        shutil.rmtree(sys.argv[1])

    os.makedirs(sys.argv[1])

    tempDir = tempfile.TemporaryDirectory(prefix='servercreator').name
    subprocess.check_call(['git', 'clone', *(('-b', branch) if branch is not None else ()), 'https://github.com/MelanX/castBINGO.git', tempDir])
    print(tempDir)

    for path in copy_paths:
        source = tempDir + os.path.sep + path
        target = sys.argv[1] + os.path.sep + path
        shutil.copytree(source, target)

    os.makedirs(sys.argv[1] + os.path.sep + 'mods')

    with open(tempDir + os.path.sep + 'manifest.json', mode='r') as file:
        manifest = json.load(file)
    mods = manifest["files"]
    for mod in mods:
        projectID = mod["projectID"]
        fileID = mod["fileID"]
        download_url = f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}/download-url"
        request1 = Request(download_url)
        response1 = urlopen(request1)
        file_url = response1.read().decode('utf-8')
        request2 = Request(file_url)
        response2 = urlopen(request2)

        print('Downloading mod %s...' % file_url[file_url.rfind('/') + 1:])

        with open(sys.argv[1] + os.path.sep + 'mods' + os.path.sep + file_url[file_url.rfind('/') + 1:], mode='wb') as target:
            target.write(response2.read())

    # Delete temp directory
    shutil.rmtree(tempDir)


if __name__ == '__main__':
    main()
