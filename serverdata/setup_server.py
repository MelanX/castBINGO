#!/usr/bin/env python3
import json
import os
import subprocess
from urllib.request import Request, urlopen


def downloadMods():
    mods = []
    with open('server.txt') as file:
        for entry in file.read().split('\n'):
            if not entry.strip() == '':
                mods.append([x.strip() for x in entry.split('/')])

    print('Install Forge')
    mcv = mods[0][0]
    mlv = mods[0][1]
    request = Request(
        f'https://files.minecraftforge.net/maven/net/minecraftforge/forge/{mcv}-{mlv}/forge-{mcv}-{mlv}-installer.jar'
    )
    response = urlopen(request)
    with open('installer.jar', mode='wb') as file:
        file.write(response.read())
    subprocess.check_call(['java', '-jar', 'installer.jar', '--installServer'])
    try:
        os.remove('installer.jar')
        os.remove('installer.jar.log')
    except FileNotFoundError:
        pass
    try:
        os.rename(f'forge-{mcv}-{mlv}.jar', 'forge.jar')
        os.rename(f'minecraft_server.{mcv}.jar', 'minecraft.jar')
        os.rename(f'{mcv}.json', 'minecraft.json')

        print('Pretty minecraft.json')
        with open('minecraft.json') as file:
            minecraft_json = json.loads(file.read())
        os.remove('minecraft.json')
        with open('minecraft.json', mode='w') as file:
            file.write(json.dumps(minecraft_json, indent=4))
    except FileNotFoundError:
        print('Failed to rename forge installer output. Forge seems to have changed their installer.')

    print('Download Mods')
    if not os.path.isdir('mods'):
        os.makedirs('mods')
    for mod in mods[1:]:
        projectID = mod[0]
        fileID = mod[1]
        download_url = f'https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}/download-url'
        request1 = Request(download_url)
        response1 = urlopen(request1)
        file_url = response1.read().decode('utf-8')
        request2 = Request(file_url.replace(' ', '%20'))
        response2 = urlopen(request2)
        print('Downloading mod %s...' % file_url[file_url.rfind('/') + 1:])
        with open('mods' + os.path.sep + file_url[file_url.rfind('/') + 1:],
                  mode='wb') as target:
            target.write(response2.read())


if __name__ == '__main__':
    downloadMods()
