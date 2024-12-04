from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.factory import factories
from config import config


class MenuKeyboards:

    @staticmethod
    def create_wallet_generation_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Generate new wallet",
                callback_data="1"
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_menu_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Open App",
                web_app=WebAppInfo(url=config.app.client_url)
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="🚀 Fast Buy",
                callback_data=factories.order.creation(action="new_order").pack()
            ),
            InlineKeyboardButton(
                text="🔫 Limit Order",
                callback_data=factories.order.creation(action="new_order").pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="👛 Wallet",
                callback_data="user_wallet"
            ),
            InlineKeyboardButton(
                text="💼 Positions",
                callback_data="user_orders"
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="⚙️ Settings",
                callback_data="settings"
            )
        )

        return markup.as_markup()
