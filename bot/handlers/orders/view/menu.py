from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards import keyboards
from bot.texts import texts
from database.db import Database

menu_router = Router()


@menu_router.callback_query(F.data == "user_orders")
async def _(
        query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        db: Database
):
    user_id = query.from_user.id

    await state.clear()

    await open_user_orders_menu(db, user_id, bot, query.message.message_id)

    await query.answer()


async def open_user_orders_menu(db: Database, user_id: int, bot: Bot, message_id) -> None:
    orders = await db.limit_orders.get_orders(user_id)

    active_orders = filter(lambda order: order.status == "active", orders)

    await bot.edit_message_text(
        chat_id=user_id,
        text=texts.orders.VIEW,
        reply_markup=keyboards.orders.create_view_orders_markup(active_orders),
        message_id=message_id
    )

