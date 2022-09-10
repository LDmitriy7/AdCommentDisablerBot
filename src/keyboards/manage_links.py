from aiogram.types import InlineKeyboardMarkup
from aiogram_utils.keyboards import InlineKeyboardButton


class ManageLinks(InlineKeyboardMarkup):
    ADD_LINK = InlineKeyboardButton('Добавить ссылку', callback_data='manage_links:add_link')
    DEL_LINK = InlineKeyboardButton('Удалить ссылку', callback_data='manage_links:del_link')

    def __init__(self):
        super().__init__(row_width=1)

        self.add(
            self.ADD_LINK,
            self.DEL_LINK,
        )
