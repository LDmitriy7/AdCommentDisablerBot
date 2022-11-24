from typing import Union

from aiogram import types
from aiogram.types import MessageEntityType

import api


def is_forward_from_linked_channel(msg: types.Message) -> bool:
    return bool(msg.is_automatic_forward)


def is_ad_post(msg: types.Message) -> bool:
    if msg.poll:
        return True

    for e in msg.entities + msg.caption_entities:
        if e.type in [MessageEntityType.MENTION, MessageEntityType.URL, MessageEntityType.TEXT_LINK]:
            return True

    if msg.reply_markup and msg.reply_markup.inline_keyboard:
        for row in msg.reply_markup.inline_keyboard:
            for button in row:
                if button.url:
                    return True

    return False


def contain_single_link(msg: types.Message) -> Union[bool, dict]:
    if len(msg.entities) != 1:
        return False

    entity = msg.entities[0]

    if not (entity.offset == 0 and entity.length == len(msg.text)):
        return False

    if entity.type == MessageEntityType.MENTION:
        return {'link': api.username_to_url(msg.text)}
    if entity.type == MessageEntityType.URL:
        return {'link': msg.text}

    return False
