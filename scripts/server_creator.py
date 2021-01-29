#!/usr/bin/env python

import json
import os
import shutil
import subprocess
import sys
import tempfile
from urllib.request import urlopen, Request


def main():
    branch = None

    if len(sys.argv) == 1:
        print('Please specify destination path as argument')
        sys.exit(1)

    if len(sys.argv) > 3:
        print('Too many arguments. Should only be "file" "path/to/destination" "branch name".')
        sys.exit()

    if os.path.isdir(sys.argv[1]):
        shutil.rmtree(sys.argv[1])

    if len(sys.argv) == 3:
        branch = str(sys.argv[2])

    os.makedirs(sys.argv[1])

    tempDir = tempfile.TemporaryDirectory(prefix='servercreator').name
    subprocess.check_call(
        ['git', 'clone', *(('-b', branch) if branch is not None else ()), 'https://github.com/MelanX/castBINGO.git',
         tempDir])

    overrides = []
    with open(tempDir + os.path.sep + 'overrides.txt') as f:
        overrides = [x.strip() for x in f.read().split('\n')]

    clientmods = []
    with open(tempDir + os.path.sep + 'clientmods.txt') as f:
        clientmods = [int(x.strip()) for x in f.read().split('\n')]

    for path in overrides:
        source = tempDir + os.path.sep + path
        target = sys.argv[1] + os.path.sep + path
        if os.path.isdir(source):
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)

    os.makedirs(sys.argv[1] + os.path.sep + 'mods')

    with open(tempDir + os.path.sep + 'manifest.json', mode='r') as f:
        manifest = json.load(f)
    mods = manifest["files"]
    for mod in mods:
        projectID = mod["projectID"]
        fileID = mod["fileID"]
        download_url = f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/f/{fileID}/download-url"
        request1 = Request(download_url)
        response1 = urlopen(request1)
        file_url = response1.read().decode('utf-8')

        if projectID in clientmods:
            print('Skipping client mod %s...' % file_url[file_url.rfind('/') + 1:])
        else:
            request2 = Request(file_url)
            response2 = urlopen(request2)
            print('Downloading mod %s...' % file_url[file_url.rfind('/') + 1:])
            with open(sys.argv[1] + os.path.sep + 'mods' + os.path.sep + file_url[file_url.rfind('/') + 1:],
                      mode='wb') as target:
                target.write(response2.read())

    with open(sys.argv[1] + os.path.sep + 'server.properties', mode='w') as f:
        f.writelines([
            'allow-flight=true\n',
            'enable-command-block=true\n',
            'max-players=32\n',
            f'motd=§l§CastBingo {manifest["version"]}§r\\nHosted by Syncopsta\n',
            'online-mode=true\n',
            'spawn-protection=0\n',
            'view-distance=8\n'
        ])

    with open(sys.argv[1] + os.path.sep + 'eula.txt', mode='w') as f:
        f.writelines([
            '#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).\n'
            'eula=true\n'
        ])

    # Delete temp directory
    shutil.rmtree(tempDir)


if __name__ == '__main__':
    main()
