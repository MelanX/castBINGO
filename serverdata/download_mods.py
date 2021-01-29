#!/usr/bin/env python3

import os
from urllib.request import Request, urlopen

def downloadMods():
    if not os.path.isdir('mods'):
        os.makedirs('mods')
    mods = []
    with open('servermods.txt') as file:
        for entry in file.read().split('\n'):
            if not entry.strip() == '':
                mods.append([x.strip() for x in entry.split('/')])
    for mod in mods:
        projectID = mod[0]
        fileID = mod[1]
        download_url = f'https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}/download-url'
        request1 = Request(download_url)
        response1 = urlopen(request1)
        file_url = response1.read().decode('utf-8')
        request2 = Request(file_url)
        response2 = urlopen(request2)
        print('Downloading mod %s...' % file_url[file_url.rfind('/') + 1:])
        with open('mods' + os.path.sep + file_url[file_url.rfind('/') + 1:],
                    mode='wb') as target:
            target.write(response2.read())

if __name__ == '__main__':
    downloadMods()