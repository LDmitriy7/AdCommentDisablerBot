from aiogram import types
from aiogram.utils import exceptions

from loader import dp


@dp.errors_handler(exception=exceptions.BotBlocked)
@dp.errors_handler(exception=exceptions.MessageNotModified)
async def ignore(*_):
    return True


@dp.errors_handler(exception=exceptions.MessageCantBeDeleted)
async def ask_to_promote_me(update: types.Update, *_):
    if update.message:
        await update.message.reply('Не могу отключить комментарии, требуются права администратора в группе')
        return True
