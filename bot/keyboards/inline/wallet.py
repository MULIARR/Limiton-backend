from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class WalletKeyboards:

    @staticmethod
    def create_wallet_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Import seed phrase",
                callback_data="import_wallet"
            )
        )

        markup.row(InlineKeyboardButton(text="‹ Back", callback_data='back_to_menu'))

        return markup.as_markup()
