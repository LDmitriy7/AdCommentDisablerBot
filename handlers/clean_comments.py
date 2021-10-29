from aiogram import types
from aiogram.types import MessageEntityType

import filters
from loader import dp


@dp.message_handler(filters.is_forwarded_from_linked_channel, content_types=types.ContentTypes.ANY)
async def clean_comments(msg: types.Message):
    for e in msg.entities + msg.caption_entities:
        if e.type in [MessageEntityType.MENTION, MessageEntityType.URL, MessageEntityType.TEXT_LINK]:
            await msg.delete()
            return

    if msg.reply_markup:
        for row in msg.reply_markup.inline_keyboard:
            for button in row:
                if button.url:
                    await msg.delete()
                    return
