import time

import pyrogram.types
from pyrogram import Client
from pyrogram.types import User
import config
import asyncio
from main import bot

client = Client("user", config.API_ID, config.API_HASH)
client.start()


async def spam_direct():
    already = [i.chat.id for i in await client.get_dialogs()]
    chat = [i.user.id for i in await client.get_chat_members("nijerinka_RF", limit=200) if
            i.user.is_bot == False and i.user.id not in already]
    good = 0
    bad = 0

    for user in chat:
        try:
            await client.send_message(user, f'Продаю бота для рассылки')
            await asyncio.sleep(30)
            good += 1
        except Exception as e:
            print(e)
            bad += 1
            continue
    print(good, bad)


async def add_members():
    chat = [i.user.id for i in await client.get_chat_members("chat_arts", limit=200)]
    g = await client.get_chat('dsfsf42123')
    g = g.id
    for i in chat:
        try:
                await client.add_chat_members(g, i)
                print(f'Успешно добавлено {i}')
                await asyncio.sleep(60)

        except Exception as e:
            print(f'Не успешно добавлено {i}, {e}')
            pass


async def get_chats():
    list = []
    async for dialog in client.iter_dialogs():
        if dialog.chat.type == 'supergroup':
            list.append({'title': dialog.chat.first_name or dialog.chat.title, 'id': dialog.chat.id})
    return list


async def leave_from_channel(id):
    try:
        await client.leave_chat(id)
        return True
    except:
        return False


async def spamming(spam_list, settings, db):
    if settings[4] == 1:
        for chat in spam_list:
            settings = db.settings()
            try:
                with open(f'{config.DIR}{settings[1]}', 'rb') as photo:
                    await client.send_photo(chat['id'], photo, caption=f"{settings[2]}\n\n{chat['text']}")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
            except Exception as e:
                try:
                    await client.send_message(chat['id'], f"{settings[2]}\n\n{chat['text']}")
                    await bot.send_message(config.ADMIN, f'[LOG] Cообщение в {chat["title"]} было успешно отправленно.')
                except Exception as e:
                    await bot.send_message(config.ADMIN,
                                           f'[LOG] Cообщение в {chat["title"]} не было отправлено из-за ошибки: {e}')
            await asyncio.sleep(settings[5] * 60)
            if settings[4] != 1:
                break
        await bot.send_message(config.ADMIN, '[LOG] Рассылка окончена')
