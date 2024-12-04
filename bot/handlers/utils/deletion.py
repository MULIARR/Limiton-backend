from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

deletion_router = Router()


@deletion_router.callback_query(F.data == 'delete_message')
async def _(query: CallbackQuery, bot: Bot):
    await bot.delete_message(
        chat_id=query.message.chat.id,
        message_id=query.message.message_id
    )

    await query.answer()
