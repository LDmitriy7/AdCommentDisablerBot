from aiogram import types

import filters
from loader import dp
from models import documents


@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def remember_ad_post(msg: types.Message):
    if not filters.is_post_ad(msg):
        if msg.reply_to_message and filters.is_post_ad(msg.reply_to_message):
            documents.AdPost(chat_id=msg.chat.id, message_id=msg.message_id).save()


@dp.message_handler(filters.is_forward_from_linked_channel, content_types=types.ContentTypes.ANY)
async def disable_comments(msg: types.Message):
    if filters.is_post_ad(msg):
        await msg.delete()
        return

    if not (msg.forward_from_chat and msg.forward_from_message_id):
        return

    ad_post: documents.AdPost = documents.AdPost.objects(
        chat_id=msg.forward_from_chat.id,
        message_id=msg.forward_from_message_id,
    ).first()

    if ad_post:
        ad_post.delete()
        await msg.delete()
