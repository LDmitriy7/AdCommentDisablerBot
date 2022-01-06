from aiogram import types

import api
import filters
from loader import dp
from models import documents


@dp.channel_post_handler(content_types=types.ContentTypes.ANY)
async def create_ad_post_document(msg: types.Message):
    if api.is_post_ad(msg) or msg.reply_to_message and api.is_post_ad(msg.reply_to_message):
        documents.AdPost(chat_id=msg.chat.id, message_id=msg.message_id).save()


@dp.message_handler(content_types=types.ContentTypes.ANY, chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def delete_ad_post_from_group(msg: types.Message):
    print(msg)

    if not await filters.is_forwarded_from_linked_channel(msg):
        return

    ad_post: documents.AdPost = documents.AdPost.objects(
        chat_id=msg.forward_from_chat.id,
        message_id=msg.forward_from_message_id,
    ).first()

    if ad_post:
        ad_post.delete()
        await msg.delete()
