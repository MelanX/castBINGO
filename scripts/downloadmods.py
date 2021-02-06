import json
import os
import shutil
from urllib.request import Request, urlopen


def main():
    with open('manifest.json') as file:
        manifest = json.loads(file.read())
    if os.path.isdir('mods'):
        shutil.rmtree('mods')
    os.makedirs('mods')
    for mod in manifest['files']:
        projectID = mod['projectID']
        fileID = mod['fileID']
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
    main()