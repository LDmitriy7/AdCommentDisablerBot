from aiogram import types
from aiogram.types import MessageEntityType


def is_post_ad(msg: types.Message) -> bool:
    for e in msg.entities + msg.caption_entities:
        if e.type in [MessageEntityType.MENTION, MessageEntityType.URL, MessageEntityType.TEXT_LINK]:
            return True

    if msg.reply_markup:
        for row in msg.reply_markup.inline_keyboard:
            for button in row:
                if button.url:
                    return True

    return False
