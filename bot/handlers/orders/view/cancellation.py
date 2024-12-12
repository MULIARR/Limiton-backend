from aiogram import Router, Bot
from aiogram.types import CallbackQuery

from bot.handlers.orders.view.menu import open_user_orders_menu
from bot.keyboards import factories
from clients import ton
from database.db import Database

cancellation_router = Router()


@cancellation_router.callback_query(factories.order.cancellation.filter())
async def _(
        query: CallbackQuery,
        bot: Bot,
        callback_data: factories.order.cancellation,
        db: Database
):
    user_id = query.from_user.id
    order_id = callback_data.order_id

    await db.limit_orders.update_order_status(order_id, OrderStatus.CANCELLED.value)

    await open_user_orders_menu(db, user_id, bot, query.message.message_id)

    await query.answer()

    # stop task
    is_cancelled = ton.order_tasks.cancel_task(order_id)
