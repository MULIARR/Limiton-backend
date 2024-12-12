from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards import keyboards
from bot.texts import texts

from bot.filters.private_chat import IsPrivateChatFilter
from clients import ton
from database.db import Database
from utils.format_number import format_number

starting_router = Router()


@starting_router.message(CommandStart(), IsPrivateChatFilter())
async def _(message: Message, bot: Bot, state: FSMContext, db: Database):
    user_id = message.from_user.id

    await state.clear()

    if not await db.users.user_exists(user_id):

        user_db_model = await db.users.add_user(user_id, message.from_user.language_code)

        # generate address
        mnemonics = ton.wallets.create_wallet()
        await db.ton_wallets.add_wallet(user_id, mnemonics)

        # admin log
        user_tg = await bot.get_chat(user_id)

        # await bot.send_message(
        #     chat_id=Chats.ADMIN,
        #     text=texts.log.NEW_USER.format(
        #         username=user_tg.username,
        #         first_name=user_tg.first_name
        #     ),
        #     message_thread_id=AdminTopics.NEW_USERS.value,
        #     disable_web_page_preview=True
        # )
    else:
        user_db_model = await db.users.get_user(user_id)

    await bot.send_message(
        chat_id=user_id,
        text=texts.menu.MENU.format(
            wallet_interface='wallet_v4_v2',
            wallet_address='Tfsgv...IHDhiJ',
            ton_balance=format_number(126.222),
            balance_in_usd=format_number(890.3442)
        ),
        reply_markup=keyboards.menu.create_menu_markup()
    )


def get_starting_text() -> str:
    ...


@starting_router.callback_query(F.data == "back_to_menu")
async def _(query: CallbackQuery, bot: Bot, state: FSMContext):
    if state:
        await state.clear()

    await bot.edit_message_text(
        chat_id=query.from_user.id,
        text=texts.menu.MENU,
        message_id=query.message.message_id,
        reply_markup=keyboards.menu.create_menu_markup()
    )

    await query.answer()
