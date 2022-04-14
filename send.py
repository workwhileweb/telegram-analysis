#!/usr/bin/python

import configparser
import json
import sys

from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("config.ini")

inputName = 'input.json'
if len(sys.argv) >= 2:
    inputName = sys.argv[1]

with open(inputName, "r", encoding='utf-8') as read_file:
    input = json.load(read_file)

api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])

client = TelegramClient(input['username'], api_id, api_hash)


async def get_group_id(client, name):
    async for dialog in client.iter_dialogs():
        if(name in dialog.name):
            return dialog.id
    return ''


async def main():
    me = await client.get_me()
    print("{} - {}".format(me.username, me.phone))

    group_id = input['chat_name']
    if(group_id != 'me'):
        group_id = await get_group_id(client, input['chat_name'])

    if(input['image'] == ''):
        await client.send_message(group_id, input['message'])
    else:
        await client.send_file(group_id, input['image'], caption=input['message'])

    result = {
        'result': 'success',
        'group_id': group_id,
        'chat_name': input['chat_name'],
        'message': input['message'],
        'username': me.username,
        'phone': me.phone
    }

    print(json.dumps(result, indent=4, sort_keys=True))
    with open(inputName + '.out', 'w', encoding='utf-8') as json_file:
        json.dump(result, json_file)


with client:
    client.loop.run_until_complete(main())
