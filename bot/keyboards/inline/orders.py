from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards.factory import factories
from database.schema import Order
from utils.format_number import format_number


class OrdersKeyboards:

    @staticmethod
    def create_order_creation_markup(order) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text=f"📤 Send: {format_number(order.send_token.amount)} {order.send_token.symbol}",
                callback_data=factories.order.creation(action="setup_send_token").pack()
            )
        )

        if order.receive_token:
            markup.row(
                InlineKeyboardButton(
                    text="↑↓",
                    callback_data=factories.order.creation(action="swap").pack()
                )
            )

            markup.row(
                InlineKeyboardButton(
                    text=f"📥 Receive: {format_number(order.receive_token.amount)} {order.receive_token.symbol}",
                    callback_data=factories.order.creation(action="setup_receive_token").pack()
                )
            )
        else:
            markup.row(
                InlineKeyboardButton(
                    text="Select Receive Token",
                    callback_data=factories.order.creation(action="select_receive_token").pack()
                )
            )

        markup.row(
            InlineKeyboardButton(
                text=f"Slippage: {order.slippage}%",
                callback_data=factories.order.creation(action="slippage").pack()
            )
        )

        if order.warning:
            markup.row(
                InlineKeyboardButton(
                    text=f"· {order.warning} ·",
                    callback_data=factories.order.creation(action="warning").pack()
                )
            )
        else:
            markup.row(
                InlineKeyboardButton(
                    text="🚀 Confirm Order ›",
                    callback_data=factories.order.creation(action="confirm").pack()
                )
            )

        markup.row(InlineKeyboardButton(text="‹ Back", callback_data='back_to_menu'))

        return markup.as_markup()

    @staticmethod
    def create_setup_token_markup(setting_up_send_token: bool) -> InlineKeyboardMarkup:

        text = "send" if setting_up_send_token else "receive"

        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text=f"Enter new {text} amount",
                callback_data=factories.order.creation(
                    action="amount_send_token" if setting_up_send_token else "amount_receive_token"
                ).pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="Change token",
                callback_data=factories.order.creation(
                    action="select_send_token" if setting_up_send_token else "select_receive_token"
                ).pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data=factories.order.creation_factory(action="back_to_order").pack()
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_back_to_order_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data=factories.order.creation_factory(action="back_to_order").pack()
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_view_orders_markup(orders: list[Order]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        for order in orders:
            markup.row(
                InlineKeyboardButton(
                    text=f"{order.send_amount} » {order.receive_amount}",  # noqa
                    callback_data=factories.order.view_factory(order_id=order.order_id).pack()
                )
            )

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data="back_to_menu"
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_view_specific_order_markup(order_id: str) -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Cancel order",
                callback_data=factories.order.cancellation(order_id=order_id).pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data="user_orders"
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_order_confirmation_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="Create Order ✅",
                callback_data=factories.order.creation_factory(action="create").pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data=factories.order.creation_factory(action="back_to_order").pack()
            )
        )

        return markup.as_markup()

    @staticmethod
    def create_slippage_markup() -> InlineKeyboardMarkup:
        markup = InlineKeyboardBuilder()

        markup.row(
            InlineKeyboardButton(
                text="1%",
                callback_data=factories.order.slippage(slippage=1).pack()
            ),
            InlineKeyboardButton(
                text="2%",
                callback_data=factories.order.slippage(slippage=2).pack()
            ),
            InlineKeyboardButton(
                text="5%",
                callback_data=factories.order.slippage(slippage=5).pack()
            )
        )

        markup.row(
            InlineKeyboardButton(
                text="‹ Back",
                callback_data=factories.order.creation_factory(action="back_to_order").pack()
            )
        )

        return markup.as_markup()
