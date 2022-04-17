#!/usr/bin/python

import configparser
import json
import sys

from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("config.ini")

inputName = config['inputNameDef']

if len(sys.argv) >= 2:
    inputName = sys.argv[1]

with open(inputName, "r", encoding='utf-8') as read_file:
    input = json.load(read_file)

apiId = config['Telegram']['apiId']
apiHash = str(config['Telegram']['apiHash'])

client = TelegramClient(input['UserName'], apiId, apiHash)


async def get_group_id(client, name):
    async for dialog in client.iter_dialogs():
        if(name in dialog.name):
            return dialog.id
    return ''


async def main():
    me = await client.get_me()
    print("{} - {}".format(me.username, me.phone))

    group_id = input['ChatId']
    if(group_id == ''):
        group_id = input['ChatName']
    if(group_id != 'me'):
        group_id = await get_group_id(client, input['ChatName'])

    if(input['Image'] == ''):
        await client.send_message(group_id, input['Caption'])
    else:
        await client.send_file(group_id, input['Image'], caption=input['Caption'])

    outputName = inputName + '.out'

    result = {
        'result': 'success',
        'ChatId': group_id,
        'ChatName': input['ChatName'],
        'Caption': input['Caption'],
        'UserName': me.username,
        'Phone': me.phone,
        'Output': outputName,
        'Input': inputName,
    }

    print(json.dumps(result, indent=4, sort_keys=True))
    with open(outputName, 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file)


with client:
    client.loop.run_until_complete(main())
