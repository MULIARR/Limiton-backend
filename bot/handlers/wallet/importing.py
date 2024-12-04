from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards import keyboards
from database.db import Database

importing_router = Router()


@importing_router.callback_query(F.data == "import_wallet")
async def _(
        query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        db: Database
):
    user_id = query.from_user.id

    await state.clear()

    wallet = await db.ton_wallets.get_selected_wallet(user_id)

    await bot.send_message(
        chat_id=user_id,
        text=f"<code>{' '.join(word for word in wallet.mnemonics)}</code>",
        reply_markup=keyboards.utils.create_deletion_markup()
    )
