from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import commands
import filters
import keyboards as kb
import texts
from loader import dp
from models import documents


class ManageLinksStates(StatesGroup):
    add_link = State()
    del_link = State()


@dp.message_handler(commands=commands.ALLOWED_LINKS, is_chat_admin=True)
async def show_allowed_links(msg: types.Message):
    chat_allowed_links: documents.ChatAllowedLinks = documents.ChatAllowedLinks.objects(chat_id=msg.chat.id).first()

    if not (chat_allowed_links and chat_allowed_links.allowed_links):
        text = 'Нет разрешенных ссылок'
    else:
        _text = [f'• {l}' for l in chat_allowed_links.allowed_links]
        text = 'Разрешенные ссылки:\n' + '\n'.join(_text)

    await msg.answer(text, disable_web_page_preview=True, reply_markup=kb.ManageLinks())


@dp.callback_query_handler(button=kb.ManageLinks.ADD_LINK, is_chat_admin=True)
async def ask_for_link_to_add(query: types.CallbackQuery):
    await ManageLinksStates.add_link.set()
    await query.message.answer(texts.ask_for_link_to_add)


@dp.callback_query_handler(button=kb.ManageLinks.DEL_LINK, is_chat_admin=True)
async def ask_for_link_to_del(query: types.CallbackQuery):
    await ManageLinksStates.del_link.set()
    await query.message.answer(texts.ask_for_link_to_del)


@dp.callback_query_handler(is_chat_admin=True, state=ManageLinksStates)
async def ask_for_link_or_cancel(query: types.CallbackQuery):
    await query.message.answer(texts.ask_for_link_or_cancel)


@dp.message_handler(is_chat_admin=True, state=ManageLinksStates.add_link)
async def add_link(msg: types.Message, state: FSMContext):
    result = filters.contain_single_link(msg)

    if not result:
        await msg.answer('Отправь мне только одну ссылку')
        return

    link: str = result['link']

    _chat_allowed_links = documents.ChatAllowedLinks.objects(chat_id=msg.chat.id)
    chat_allowed_links = _chat_allowed_links.first() or documents.ChatAllowedLinks(chat_id=msg.chat.id)

    if link in chat_allowed_links.allowed_links:
        await msg.answer('Эта ссылка уже есть в списке')
        await state.finish()
        return

    chat_allowed_links.allowed_links.append(link)
    chat_allowed_links.save()

    await msg.answer('Ссылка добавлена в список')
    await state.finish()


@dp.message_handler(is_chat_admin=True, state=ManageLinksStates.del_link)
async def del_link(msg: types.Message, state: FSMContext):
    result = filters.contain_single_link(msg)

    if not result:
        await msg.answer('Отправь мне только одну ссылку')
        return

    link: str = result['link']

    _chat_allowed_links = documents.ChatAllowedLinks.objects(chat_id=msg.chat.id)
    chat_allowed_links = _chat_allowed_links.first() or documents.ChatAllowedLinks(chat_id=msg.chat.id)

    if link not in chat_allowed_links.allowed_links:
        await msg.answer('Такой ссылки нет в списке')
        await state.finish()
        return

    chat_allowed_links.allowed_links.remove(link)
    chat_allowed_links.save()

    await msg.answer('Ссылка удалена из списка')
    await state.finish()
