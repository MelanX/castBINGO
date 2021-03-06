#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
from urllib.request import Request, urlopen

import gitignore_parser

import update_emotes
import modlist
import changelog_creator

MOD_LIST_CREATOR_VERSION = '1.2.0'


def main():
    with open('tokens.json') as file:
        token = json.loads(file.read())['github']

    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()

    with open('pack.json') as file:
        manifest = json.loads(file.read())

    print(f'Prepare Release v{manifest["version"]} on commit {commit}')

    print('Delete old build data')
    if os.path.isdir('build'):
        shutil.rmtree('build')
    os.makedirs('build')

    print('Read gitignore')
    gitignore = gitignore_parser.parse_gitignore('.gitignore', '.')

    print('Generate manifest')
    modlist.generateManifest()
    with open('manifest.json') as file:
        manifest = json.loads(file.read())

    print('Creating changelog')
    changelog_creator.main(manifest)

    print('Update emotes')
    update_emotes.updateEmotes()

    print('Download ModListCreator')
    request = Request(
        f'https://github.com/MelanX/ModListCreator/releases/download/v{MOD_LIST_CREATOR_VERSION}/ModListCreator-{MOD_LIST_CREATOR_VERSION}.jar'
    )
    response = urlopen(request)
    with open(os.path.join('build', 'ModListCreator.jar'), mode='wb') as file:
        file.write(response.read())

    print('Update root directory modlist.')
    subprocess.check_call(
        ['java', '-jar', os.path.join('build', 'ModListCreator.jar'),
         '--md',
         '--manifest', 'manifest.json',
         '--output', '.',
         '--detailed']
    )

    print('Prepare CurseForge pack.')
    createModpackZip(manifest, gitignore)

    print('Prepare Server zips.')
    createServerZip(manifest, gitignore, 'default')
    createServerZip(manifest, gitignore, 'skyblock')

    print('Uploading to GitHub')
    uploadToGithub(token, manifest)

    print('Done')


def createModpackZip(manifest, gitignore):
    targetDir = os.path.join('build', 'curseforge')

    os.makedirs(targetDir)
    shutil.copy2('manifest.json', targetDir + os.path.sep + 'manifest.json')

    print('Generate ModList')
    subprocess.check_call(
        ['java', '-jar', os.path.join('build', 'ModListCreator.jar'),
         '--html',
         '--manifest', targetDir + os.path.sep + 'manifest.json',
         '--output', targetDir]
    )

    print('Copy overrides')
    with open('overrides.txt') as file:
        overrides = [x.strip() for x in file.read().split('\n')]
    shutil.copytree(os.path.join('build', 'overrides'), targetDir + os.path.sep + manifest['overrides'])
    for entry in overrides:
        copyNotGitignoreTree('.', targetDir + os.path.sep + manifest['overrides'], entry, gitignore)

    print('Create archive')
    shutil.make_archive(os.path.join('build', 'curseforge'), 'zip', targetDir)

def createServerZip(manifest, gitignore, edition):
    print("Creating server zip for edition " + edition)
    targetDir = os.path.join('build', 'server', edition)

    os.makedirs(targetDir)

    print('Create server ModList')
    clientmods = []
    with open('clientmods.txt') as file:
        clientmods = [int(x.strip()) for x in file.read().split('\n')]
    with open(targetDir + os.path.sep + 'server.txt', mode='w') as file:
        mcv = manifest['minecraft']['version']
        mlv: str = manifest['minecraft']['modLoaders'][0]['id']
        if mlv.startswith('forge-'):
            mlv = mlv[6:]
        file.write(f'{mcv}/{mlv}\n')
        for mod in manifest['files']:
            if not mod['projectID'] in clientmods:
                file.write(f'{mod["projectID"]}/{mod["fileID"]}\n')

    print('Copy server files')
    shutil.copytree('serverdata', targetDir, dirs_exist_ok=True)

    print('Copy overrides')
    with open('overrides.txt') as file:
        overrides = [x.strip() for x in file.read().split('\n')]
    shutil.copytree(os.path.join('build', 'overrides'), targetDir, dirs_exist_ok=True)
    for entry in overrides:
        copyNotGitignoreTree('.', targetDir, entry, gitignore)

    if os.path.isdir('server-' + edition):
        print('Copy edition specific server files')
        shutil.copytree('server-' + edition, targetDir, dirs_exist_ok=True)

    print('Generate server files')
    with open(targetDir + os.path.sep + 'server.properties', mode='w') as f:
        f.writelines([
            'allow-flight=true\n',
            'enable-command-block=true\n',
            'max-players=32\n',
            f'motd=§4CastBingo {manifest["version"]}{(" " + edition.capitalize() + " Edition") if edition != "default" else ""}§r\\nHosted by Syncopsta\n',
            'online-mode=true\n',
            'spawn-protection=0\n',
            'view-distance=8\n',
            'enable-query=true\n',
            'query.port=25565\n'
        ])

    print('Create archive')
    shutil.make_archive(os.path.join('build', 'server', edition), 'zip', targetDir)

def copyNotGitignoreTree(sourceBase: str, targetBase: str, relative: str, gitignore):
    source = sourceBase + os.path.sep + relative
    target = targetBase + os.path.sep + relative
    if os.path.isdir(source):
        for child in os.listdir(source):
            copyNotGitignoreTree(sourceBase, targetBase, relative + os.path.sep + child, gitignore)
    else:
        if not gitignore(relative):
            if not os.path.isdir(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            shutil.copy2(source, target)

def uploadToGithub(token, manifest):
    print('Push latest changes to GitHub')
    subprocess.check_call(['git', 'add', '.'])
    subprocess.check_call(['git', 'commit', '-m', f'v{manifest["version"]} release'])
    subprocess.check_call(['git', 'push'])
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()

    print(f'Create release on newer commit {commit}')
    create_release = Request('https://api.github.com/repos/MelanX/castBINGO/releases', method='POST')
    create_release.add_header('Authorization', f'token {token}')
    create_release.add_header('Accept', 'application/vnd.github.v3+json')
    create_release.add_header('Content-Type', 'application/json')
    with open(f'changelogs/changelog-{manifest["version"]}.md', 'r', encoding='utf-8') as file:
        changelog = file.read()
    create_release.data = json.dumps({
        'tag_name': f'v{manifest["version"]}',
        'target_commitish': commit,
        'name': f'v{manifest["version"]}',
        'body': changelog,
        'prerelease': False
    }).encode('utf-8')
    release_id = json.loads(urlopen(create_release).read())['id']

    print('Upload CurseForge pack')
    uploadFileToRelease(token, release_id, manifest, 'application/zip', 'curseforge', 'zip', os.path.join('build', 'curseforge.zip'))

    print('Upload Server zips')
    uploadFileToRelease(token, release_id, manifest, 'application/zip', 'server-default', 'zip', os.path.join('build', 'server', 'default.zip'))
    uploadFileToRelease(token, release_id, manifest, 'application/zip', 'server-skyblock', 'zip', os.path.join('build', 'server', 'skyblock.zip'))

def uploadFileToRelease(token, release_id, manifest, mime, basename, suffix, path):
    request = Request(f'https://uploads.github.com/repos/MelanX/castBINGO/releases/{release_id}/assets?name={basename}-{manifest["version"]}.{suffix}', method='POST')
    request.add_header('Authorization', f'token {token}')
    request.add_header('Content-Type', mime)
    with open(path, mode='rb') as file:
        request.data = file.read()
    urlopen(request)

if __name__ == '__main__':
    main()
