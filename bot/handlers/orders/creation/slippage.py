from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.handlers.orders.creation.menu import open_order_creation
from bot.storages import storages as st
from bot.keyboards import factories

slippage_router = Router()


@slippage_router.callback_query(factories.order.slippage.filter())
async def _(
        query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        callback_data: factories.order.slippage,
):
    await st.limit_order.update(state, slippage=callback_data.slippage)

    await open_order_creation(bot, query.from_user.id, query.message.message_id, state)
