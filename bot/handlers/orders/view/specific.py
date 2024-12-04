from aiogram import Router, Bot
from aiogram.types import CallbackQuery

from bot.keyboards import factories, keyboards
from bot.texts import texts
from database.db import Database

specific_router = Router()


@specific_router.callback_query(factories.order.view.filter())
async def _(
        query: CallbackQuery,
        bot: Bot,
        callback_data: factories.order.view,
        db: Database
):
    user_id = query.from_user.id
    order_id = callback_data.order_id

    await bot.edit_message_text(
        chat_id=user_id,
        text=texts.orders.SPECIFIC.format(
            order_id=order_id
        ),
        reply_markup=keyboards.orders.create_view_specific_order_markup(order_id),
        message_id=query.message.message_id
    )

    await query.answer()
