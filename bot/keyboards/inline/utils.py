from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class UtilsKeyboards:
    @staticmethod
    def create_deletion_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Close",
                callback_data="delete_message"
            )
        )

        return markup.as_markup()
