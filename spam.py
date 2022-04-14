# https://docs.telethon.dev/en/stable/basic/quick-start.html

import configparser
from telethon import TelegramClient

config = configparser.ConfigParser()
config.read("config.ini")

username = config['Telegram']['username']
api_id = config['Telegram']['api_id']
api_hash = str(config['Telegram']['api_hash'])

client = TelegramClient(username, api_id, api_hash)


async def get_group_id(client, name):
    async for dialog in client.iter_dialogs():
        if(name in dialog.name):
            return dialog.id
    return ''


async def main():
    me = await client.get_me()
    # print(me.stringify())
    print("{} - {}".format(me.username, me.phone))
    # async for dialog in client.iter_dialogs():
    #    print(dialog.name, 'has ID', dialog.id)

    # await client.send_message('me', 'Hello, myself!')
    # await client.send_message(-1001612813366, 'Hello, group!')

    # while (True):
    group_id = await get_group_id(client, 'MMO-Chat')
    await client.send_message(group_id, 'Hello, group!')
    # time.sleep(100)  # seconds

    # await client.send_message('+34600123123', 'Hello, friend!')
    # await client.send_message('username', 'Testing Telethon!')

    # message = await client.send_message(
    #    'me',
    #    'This message has **bold**, `code`, __italics__ and '
    #    'a [nice website](https://example.com)!',
    #    link_preview=False
    # )
    # print(message.raw_text)
    # await message.reply('Cool!')
    # await client.send_file('me', '/home/me/Pictures/holidays.jpg')
    # async for message in client.iter_messages('me'):
    #    print(message.id, message.text)
    #    if message.photo:
    #        path = await message.download_media()
    #        print('File saved to', path)  # printed after download is done


with client:
    client.loop.run_until_complete(main())
