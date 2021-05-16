from typing import Callable

from pyrogram import Client
from pyrogram.types import Message

from helpers.admins import get_administrators
from config import SUDO_USERS


def errors(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        try:
            return await func(client, message)
        except Exception as e:
            if type(e).__name__ == "DownloadError":
              await message.reply_text("Ahh sorry looks like i am not being able to download..., please retry again or use telegram files..")
            else: 
              await message.reply(f"{type(e).__name__}: {e}")

    return decorator


def authorized_users_only(func: Callable) -> Callable:
    async def decorator(client: Client, message: Message):
        if message.from_user.id in SUDO_USERS:
            return await func(client, message)

        administrators = await get_administrators(message.chat)

        for administrator in administrators:
            if administrator == message.from_user.id:
                return await func(client, message)

    return decorator