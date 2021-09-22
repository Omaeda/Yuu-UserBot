import logging
import tempfile

import telethon
from telethon import events

from config import *

client: telethon.client = telethon.TelegramClient('session_name', api_id, api_hash)
logging.basicConfig(level=logging.INFO)


@client.on(events.NewMessage(outgoing=True, pattern=r'(^\.getids (.*))|(^xd)'))
async def handler(event: events.newmessage.NewMessage.Event):
    if "xd" in event.message.text:
        group_id = event.chat_id
    else:
        group_id = event.pattern_match.group(2)
    myself = await client.get_me()
    chat_members_id = []
    try:
        users = await client.get_participants(int(group_id), aggressive=True)
        for user in users:
            if user.bot:  # excluye a todos los bots de la lista
                continue
            if user.id == myself.id:  # excluye su propia id de la lista
                continue

            chat_members_id.append(str(user.id))

    except ValueError:
        return await event.edit("no pude acceder a ese chat verifica que el ID sea correcto")

    text = '\n'.join(chat_members_id)
    with tempfile.NamedTemporaryFile("w+", suffix=".txt") as file:
        file.write(text)
        file.seek(0)
        file.flush()
        try:
            await client.send_message("me", file=file.name)
        except telethon.errors.rpcerrorlist.FilePartsInvalidError:
            return await event.edit("no pude recolectar nada")


if __name__ == '__main__':
    with client:
        logging.info("Userbot inicido")
        client.run_until_disconnected()
