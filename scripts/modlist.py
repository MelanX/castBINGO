import hashlib
import json
import os
import zipfile
from typing import List, Dict
from urllib.request import Request, urlopen

import murmurhash2
import toml


def generateManifest():
    files = ['mods' + os.path.sep + x for x in os.listdir('mods')]
    mods = ModCache('modcache.json').get_files_info(files)
    mods.sort(key = lambda x: x['_displayName'])
    with open('pack.json') as file:
        manifest = json.loads(file.read())
    manifest['files'] = mods
    if not os.path.isdir('build'):
        os.makedirs('build')
    with open('manifest.json', mode='w') as file:
        file.write(json.dumps(manifest, indent=4) + '\n')

class ModCache:
    def __init__(self, file: str):
        self.file = file
        self.signatures = {}
        self.modid_map = {}
        if os.path.isfile(file):
            self.load()
        else:
            self.save()

    def load(self):
        with open(self.file) as f:
            data = json.loads(f.read())
        self.signatures = data['signatures']
        self.modid_map = data['modid_map']

    def save(self):
        data = {
            'signatures': self.signatures,
            'modid_map': self.modid_map
        }
        with open(self.file, mode='w') as f:
            f.write(json.dumps(data, indent=4) + '\n')

    def resolve_signature(self, signature: str):
        if signature in self.signatures:
            return self.signatures[signature]
        else:
            return None

    def resolve_modid(self, modid: str):
        if modid in self.modid_map:
            return self.modid_map[modid]
        else:
            return None

    def resolve_or_request_modid(self, modid: str, file: str):
        if modid in self.modid_map:
            return self.modid_map[modid]
        else:
            basename = os.path.basename(file)
            print(f'Failed to infer project id for file {basename}.')
            projectID = int(input('Project Id: '))
            name_request = Request(f'https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}')
            name_response = urlopen(name_request)
            name_data = json.loads(name_response.read().decode('utf-8'))
            self.modid_map[modid] = {
                '_displayName': name_data['name'],
                'projectID': projectID
            }
            return self.modid_map[modid]

    def resolve_modid_from_file(self, file):
        with zipfile.ZipFile(file) as zip:
            with zip.open('META-INF/mods.toml') as file:
                modinfo = toml.loads(file.read().decode('utf-8'))
        modids = [x['modId'].lower() for x in modinfo['mods']]
        modids.sort() # We need a unique string. And a file can contain multiple mod ids.
        return '|'.join(modids)


    def get_files_info(self, files: List[str]) -> list:
        hashes = {}
        murmur_to_md5 = {}
        murmur_to_file = {}
        for path in files:
            with open(path, mode='rb') as file:
                data = file.read()
                murmur = murmurhash2.murmurhash2(data.replace(b'\011', b'').replace(b'\012', b'').replace(b'\015', b'').replace(b'\040', b''), 1)
                md5 = hashlib.md5(data).hexdigest()
                hashes[path] = {
                    'murmur': murmur,
                    'md5': md5
                }
                murmur_to_md5[murmur] = md5
                murmur_to_file[murmur] = path
        mods = []
        murmur_resolve = []
        for entry in hashes:
            signature = self.resolve_signature(hashes[entry]['md5'])
            if signature is not None:
                mods.append(signature)
            else:
                murmur_resolve.append(hashes[entry]['murmur'])

        request = Request('https://addons-ecs.forgesvc.net/api/v2/fingerprint', method='POST')
        request.add_header('Accept', 'application/json')
        request.add_header('Content-Type', 'application/json')
        request.data = (json.dumps(murmur_resolve) + '\n').encode('utf-8')
        response = urlopen(request)
        cf_data = json.loads(response.read().decode('utf-8'))

        modid_resolve = cf_data['unmatchedFingerprints']
        for match in cf_data['exactMatches']:
            name_request = Request(f'https://addons-ecs.forgesvc.net/api/v2/addon/{match["id"]}')
            name_response = urlopen(name_request)
            name_data = json.loads(name_response.read().decode('utf-8'))
            mod_entry = {
                '_displayName': name_data['name'],
                'projectID': match['id'],
                'fileID': match['file']['id']
            }
            self.signatures[murmur_to_md5[match['file']['packageFingerprint']]] = mod_entry
            mods.append(mod_entry)

        for murmur in modid_resolve:
            file = murmur_to_file[murmur]
            modid = self.resolve_modid_from_file(file)
            mod_data = self.resolve_or_request_modid(modid, file)
            files_request = Request(f'https://addons-ecs.forgesvc.net/api/v2/addon/{mod_data["projectID"]}/files')
            files_request.add_header('Accept', 'application/json')
            files_response = urlopen(files_request)
            files_data = json.loads(files_response.read().decode('utf-8'))
            for entry in files_data:
                print(entry)
                if murmur == entry['packageFingerprint']:
                    mod_entry = {
                        '_displayName': mod_data["_displayName"],
                        'projectID': mod_data["projectID"],
                        'fileID': entry['id']
                    }
                    self.signatures[murmur_to_md5[murmur]] = mod_entry
                    mods.append(mod_entry)
                    break
            else:
                print(f'Failed to infer file id for file {os.path.basename(file)}')
                fileID = int(input('File Id: '))
                mod_entry = {
                    '_displayName': mod_data["_displayName"],
                    'projectID': mod_data["projectID"],
                    'fileID': fileID
                }
                self.signatures[murmur_to_md5[murmur]] = mod_entry
                mods.append(mod_entry)

        self.save()
        return mods


if __name__ == '__main__':
    generateManifest()
