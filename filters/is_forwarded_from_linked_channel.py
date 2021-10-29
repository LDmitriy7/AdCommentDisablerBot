from aiogram import types

from loader import dp


async def is_forwarded_from_linked_channel(msg: types.Message) -> bool:
    if not msg.forward_from_chat:
        return False

    chat = await dp.bot.get_chat(msg.chat.id)

    return msg.forward_from_chat.id == chat.linked_chat_id
