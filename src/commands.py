from contextlib import suppress

from aiogram import types
from aiogram.utils.exceptions import TelegramAPIError

import config
from loader import dp

START = 'start'
CANCEL = 'cancel'
BROADCAST = 'broadcast'
ALLOWED_LINKS = 'allowed_links'

USER_COMMANDS = [
    types.BotCommand(START, 'Запустить бота'),
]

CHAT_ADMIN_COMMANDS = USER_COMMANDS + [
    types.BotCommand(ALLOWED_LINKS, 'Разрешенные ссылки'),
    types.BotCommand(CANCEL, 'Отменить'),
]

ADMIN_COMMANDS = USER_COMMANDS + [
    # types.BotCommand(BROADCAST, 'Рассылка'),
]


async def setup():
    await dp.bot.set_my_commands(USER_COMMANDS)
    await dp.bot.set_my_commands(CHAT_ADMIN_COMMANDS, scope=types.BotCommandScopeAllChatAdministrators())

    for user_id in config.Users.admins_ids:
        with suppress(TelegramAPIError):
            await dp.bot.set_my_commands(ADMIN_COMMANDS, scope=types.BotCommandScopeChat(user_id))
