#!/usr/bin/env python3

import json
import os
import re
import shutil
import tempfile
import zipfile
from urllib.request import Request, urlopen

owner = "MelanX"
repo = "castBINGO"


def getCurrentManifest():
    print("Get current manifest...")
    response = urlopen("https://raw.githubusercontent.com/MelanX/castBINGO/master/manifest.json")
    return json.loads(response.read())


def appendFile(file, content: str = None):
    if content is None:
        file.writelines("\n\n")
    else:
        file.writelines(content + "\n")


def cleanhtml(raw_html):
    html = re.compile('<.*?>|-')
    spaces = re.compile('\\s|&nbsp;')
    cleantext = re.sub(html, '', raw_html)
    cleantext = re.sub(spaces, ' ', cleantext)
    return cleantext.strip()


def getOldMod(item, old_mods: list):
    for old_mod in old_mods:
        if item == old_mod["projectID"]:
            return old_mod
    return None


def githubChanges(manifest_data: dict):
    req_tag = Request(f"https://api.github.com/repos/{owner}/{repo}/tags")
    req_release = Request(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")

    res_tag = urlopen(req_tag)
    res_release = urlopen(req_release)

    data_tag = json.loads(res_tag.read())
    data_release = json.loads(res_release.read())

    sha = None
    for tag in data_tag:
        if tag["name"] == data_release["tag_name"]:
            sha = tag["commit"]["sha"]
            break

    if sha is None:
        return

    header = {
        "accept": "application/vnd.github.v3+json",
        "sha": sha
    }
    req_commits = Request(f"https://api.github.com/repos/{owner}/{repo}/commits", headers=header)
    res_commits = urlopen(req_commits)

    commits = []
    loads = json.loads(res_commits.read())
    for commit in loads:
        if commit["sha"] == sha:
            break
        message = commit["commit"]["message"].split("\n")[0]
        url = commit["html_url"]
        commits.append([message, url])

    file_name = f"changelogs/changelog-{manifest_data['version']}.md"
    with open(file_name, "a", encoding="utf-8") as f:
        appendFile(f, "# Changelog for castBINGO! " + manifest_data['version'])
        appendFile(f, "## Internal changes")
        for commit in commits:
            appendFile(f, f"- [{commit[0]}]({commit[1]})")


def modsChanges(new_manifest_data: dict):
    old_mods = []
    new_mods = []

    tempDir = tempfile.TemporaryDirectory(prefix="updatefiles").name
    req_release = Request(f"https://api.github.com/repos/{owner}/{repo}/releases/latest")
    res_release = urlopen(req_release)
    data = json.loads(res_release.read())
    url = data["zipball_url"]

    zip_req = Request(url)
    zip_res = urlopen(zip_req)

    os.makedirs(tempDir)
    print("Downloading zip file from latest release...")
    file = tempDir + os.path.sep + data["body"] + ".zip"
    with open(file, "wb") as f:
        f.write(zip_res.read())

    with zipfile.ZipFile(file, "r") as zip_f:
        zip_f.extractall(tempDir)

    os.remove(file)
    manifest = tempDir + os.path.sep + os.listdir(tempDir)[0] + os.path.sep + "manifest.json"
    with open(manifest, "r") as f:
        manifest_data = json.loads(f.read())

    for mod in manifest_data["files"]:
        old_mods.append({"projectID": mod["projectID"], "fileID": mod["fileID"]})

    updated = []
    downgraded = []
    removed = []
    added = []

    print("Compare old with new manifest...")
    for mod in new_manifest_data["files"]:
        new_mods.append(mod["projectID"])

        old_mod = getOldMod(mod["projectID"], old_mods)
        if old_mod:
            if mod["fileID"] == getOldMod(mod["projectID"], old_mods)["fileID"]:
                continue
            else:
                if mod["fileID"] < old_mod["fileID"]:
                    downgraded.append(mod)
                else:
                    updated.append(mod)
        else:
            added.append(mod)

    for mod in old_mods:
        if mod["projectID"] not in new_mods:
            removed.append(mod)

    if not os.path.exists("changelogs"):
        os.mkdir("changelogs")

    file_name = f"changelogs/changelog-{new_manifest_data['version']}.md"
    if os.path.isfile(file_name):
        os.remove(file_name)
    with open(file_name, "a", encoding="utf-8") as f:
        if len(updated) > 0 or len(added) > 0 or len(removed) > 0 or len(updated) > 0:
            appendFile(f, "## Mod Changes")

        old_forge = manifest_data["minecraft"]["modLoaders"][0]["id"]
        new_forge = new_manifest_data["minecraft"]["modLoaders"][0]["id"]
        if old_forge != new_forge:
            appendFile(f, "### Forge updated")
            appendFile(f, f"{old_forge} --> {new_forge}")

        if len(added) > 0:
            print("Writing newly added mods to changelog...")
            appendFile(f, "### Added")
            for mod in added:
                projectID = mod["projectID"]
                fileID = mod["fileID"]
                request = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}")
                response = urlopen(request)
                data = json.loads(response.read())
                appendFile(f, f"- [{data['name']}]({data['websiteUrl']}/files/{fileID})")
            appendFile(f)

        if len(updated) > 0:
            print("Writing updated mods to changelog...")
            appendFile(f, "### Updated")
            for mod in updated:
                projectID = mod["projectID"]
                fileID = mod["fileID"]
                old_mod_ID = getOldMod(projectID, old_mods)["fileID"]
                mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}")
                old_mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{old_mod_ID}")
                new_mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}")
                changelog_req = Request(
                    f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}/changelog")

                mod_res = urlopen(mod_req)
                old_mod_res = urlopen(old_mod_req)
                new_mod_res = urlopen(new_mod_req)
                changelog_res = urlopen(changelog_req)

                mod_data = json.loads(mod_res.read())
                old_mod_data = json.loads(old_mod_res.read())
                new_mod_data = json.loads(new_mod_res.read())

                appendFile(f,
                           f"- [{old_mod_data['displayName']}]({mod_data['websiteUrl']}/files/{old_mod_ID}) --> [{new_mod_data['displayName']}]({mod_data['websiteUrl']}/files/{fileID})")

                i = 0
                for line in changelog_res.readlines():
                    if not line.strip() == "":
                        parts = line.decode().split('<br>')
                        for part in parts:
                            if not cleanhtml(part).strip() == "":
                                if i < 5:
                                    i += 1
                                    appendFile(f, "\t- " + cleanhtml(part))
                                else:
                                    appendFile(f, "\t- And a bit more...")
                                    break
                    if i >= 5:
                        break
            appendFile(f)

        if len(downgraded) > 0:
            print("Writing downgraded mods to changelog...")
            appendFile(f, "### Downgraded")
            for mod in downgraded:
                projectID = mod["projectID"]
                fileID = mod["fileID"]
                old_mod_ID = getOldMod(projectID, old_mods)["fileID"]
                mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}")
                old_mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{old_mod_ID}")
                new_mod_req = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{projectID}/file/{fileID}")

                mod_res = urlopen(mod_req)
                old_mod_res = urlopen(old_mod_req)
                new_mod_res = urlopen(new_mod_req)

                mod_data = json.loads(mod_res.read())
                old_mod_data = json.loads(old_mod_res.read())
                new_mod_data = json.loads(new_mod_res.read())

                appendFile(f,
                           f"- [{old_mod_data['displayName']}]({mod_data['websiteUrl']}/files/{old_mod_ID}) --> [{new_mod_data['displayName']}]({mod_data['websiteUrl']}/files/{fileID})")
            appendFile(f)

        if len(removed) > 0:
            print("Writing removed mods to changelog...")
            appendFile(f, "### Removed")
            for mod in removed:
                request = Request(f"https://addons-ecs.forgesvc.net/api/v2/addon/{mod['projectID']}")
                response = urlopen(request)
                data = json.loads(response.read())
                appendFile(f, f"- [{data['name']}]({data['websiteUrl']})")

    shutil.rmtree(tempDir, ignore_errors=True)


if __name__ == '__main__':
    manifest = getCurrentManifest()
    githubChanges(manifest)
    modsChanges(manifest)
