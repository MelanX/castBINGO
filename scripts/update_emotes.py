#!/usr/bin/env python3

import json
import os
import shutil
from urllib.request import Request, urlopen

def updateEmotes():
    with open('tokens.json') as file:
        token = json.loads(file.read())['twitch']

    request = Request(f'https://id.twitch.tv/oauth2/validate')
    request.add_header('Authorization', f'OAuth {token}')
    response = urlopen(request)
    data = json.loads(response.read())
    client_id = data['client_id']

    with open('emotes.json') as file:
        emote_data = json.loads(file.read())

    emotes = {}

    for twitch_channel in emote_data['twitchChannels']:
        id = get_user_id(twitch_channel, client_id, token)
        request = Request(f'https://api.twitchemotes.com/api/v4/channels/{id}')
        response = urlopen(request)
        data = json.loads(response.read())
        for entry in data['emotes']:
            emotes[entry['code']] = f'https://static-cdn.jtvnw.net/emoticons/v1/{entry["id"]}/3.0'

    for twitch_channel in emote_data['bttvChannels']:
        id = get_user_id(twitch_channel, client_id, token)
        request = Request(f'https://api.betterttv.net/3/cached/users/twitch/{id}')
        response = urlopen(request)
        data = json.loads(response.read())
        for entry in data['sharedEmotes']: 
            emotes[entry['code']] = f'https://cdn.betterttv.net/emote/{entry["id"]}/3x.{entry["imageType"]}'
        for entry in data['channelEmotes']:
            emotes[entry['code']] = f'https://cdn.betterttv.net/emote/{entry["id"]}/3x.{entry["imageType"]}'

    for twitch_channel in emote_data['ffzChannels']:
        id = get_user_id(twitch_channel, client_id, token)
        request = Request(f'https://api.frankerfacez.com/v1/room/id/{id}')
        response = urlopen(request)
        data = json.loads(response.read())
        for set in data['sets']:
            for entry in data['sets'][set]['emoticons']:
                urls = entry["urls"]
                max = 1
                for url_key in urls:
                    if int(url_key) > max:
                        max = int(url_key)
                emotes[entry['name']] = f'https:{entry["urls"][str(max)]}'

    target_dir = os.path.join('build', 'overrides', 'kubejs',  'data', 'emojiful', 'recipes')
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)

    os.makedirs(target_dir)

    for emote in emotes:
        file_path = target_dir + os.path.sep + f'{emote.lower()}.json'
        with open(file_path, mode='w') as file:
            file.write(json.dumps({
                'category': 'Twitch_3rd_party',
                'name': emote,
                'url': emotes[emote],
                'type': 'emojiful:emoji_recipe'
            }, indent=4) + '\n')

def get_user_id(channel_name: str, client_id: str, token: str) -> str:
    request = Request(f'https://api.twitch.tv/helix/users?login={channel_name}')
    request.add_header('Client-ID', client_id)
    request.add_header('Authorization', f'Bearer {token}')
    response = urlopen(request)
    data = json.loads(response.read())
    return data['data'][0]['id']

if __name__ == '__main__':
    updateEmotes()