from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.storages import storages as st
from bot.keyboards import keyboards, factories
from bot.states.order import PasteCAState, EnterAmount
from bot.texts import texts
from clients import ton
from database.db import Database

menu_router = Router()


@menu_router.callback_query(factories.order.creation.filter())
async def _(
        query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        callback_data: factories.order,
        db: Database
):
    user_id = query.from_user.id
    message_id = query.message.message_id

    # get out of the state
    await state.set_state(state=None)

    # get order storage model
    order = await st.limit_order.get(state)

    if callback_data.action in ("new_order", "back_to_order"):
        await open_order_creation(bot, user_id, message_id, state)

    elif callback_data.action in ("setup_send_token", "setup_receive_token"):
        setting_up_send_token = True if callback_data.action == "setup_send_token" else False

        await bot.edit_message_text(
            chat_id=user_id,
            text=texts.orders.SETUP_TOKEN,
            message_id=message_id,
            reply_markup=keyboards.orders.create_setup_token_markup(setting_up_send_token)
        )

    elif callback_data.action in ("amount_send_token", "amount_receive_token"):
        await bot.edit_message_text(
            chat_id=user_id,
            text=texts.orders.ENTER_AMOUNT,
            message_id=message_id,
            reply_markup=keyboards.orders.create_back_to_order_markup()
        )

        # set state
        await state.set_state(EnterAmount.enter)

        setting_up_send_token = True if callback_data.action == "amount_send_token" else False

        await st.limit_order.update(state, setting_up_send_token=setting_up_send_token, message_id=message_id)

    elif callback_data.action in ("select_send_token", "select_receive_token"):
        await bot.edit_message_text(
            chat_id=query.from_user.id,
            text=texts.orders.SELECT_RECEIVE_TOKEN,
            message_id=message_id,
            reply_markup=keyboards.orders.create_back_to_order_markup()
        )

        # set state
        await state.set_state(PasteCAState.paste)

        setting_up_send_token = True if callback_data.action == "select_send_token" else False

        await st.limit_order.update(state, setting_up_send_token=setting_up_send_token, message_id=message_id)

    elif callback_data.action == "slippage":
        await bot.edit_message_text(
            chat_id=user_id,
            text=texts.orders.SLIPPAGE,
            message_id=message_id,
            reply_markup=keyboards.orders.create_slippage_markup()
        )

    elif callback_data.action == "warning":
        await bot.answer_callback_query(query.id, text=order.warning)

    elif callback_data.action == "swap":
        await st.limit_order.update(state, send_token=order.receive_token, receive_token=order.send_token)

        await open_order_creation(bot, user_id, message_id, state)

    elif callback_data.action == "confirm":
        swap_assets = [
            {"address": order.send_token.address, "amount": order.send_token.amount},
            {"address": order.receive_token.address, "amount": order.receive_token.amount}
        ]

        minimum_to_receive_amount = order.receive_token.amount - (order.receive_token.amount * (order.slippage / 100))

        rates = await ton.jettons.get_rates_for_swap(swap_assets)

        await bot.edit_message_text(
            chat_id=user_id,
            text=texts.orders.CONFIRMATION.format(
                send_amount=order.send_token.amount,
                send_token_symbol=order.send_token.symbol,
                send_token_rate=rates.send_amount_rate_in_usd,
                receive_amount=order.receive_token.amount,
                receive_token_symbol=order.receive_token.symbol,
                receive_token_rate=rates.receive_amount_rate_in_usd,
                minimum_to_receive_amount=minimum_to_receive_amount,
                slippage=order.slippage,
                profit_in_usd=rates.profit_in_usd,
                profit_percent=rates.profit
            ),
            message_id=message_id,
            reply_markup=keyboards.orders.create_order_confirmation_markup()
        )

        await st.limit_order.update(state, minimum_to_receive=minimum_to_receive_amount)

    elif callback_data.action == "create":

        # db entry
        order = await db.limit_orders.add_order(
            user_id=user_id,
            send_amount=order.send_token.amount,
            send_token_address=order.send_token.address,
            receive_amount=order.receive_token.amount,
            receive_token_address=order.receive_token.address,
            minimum_to_receive_amount=order.minimum_to_receive,
            slippage=order.slippage
        )

        # create limit order
        limit_order = await ton.limit_orders.create_limit_order_model(order)

        # launch limit order
        await ton.limit_orders.launch_limit_order(limit_order)

        await bot.edit_message_text(
            chat_id=user_id,
            text=texts.orders.CREATED,
            message_id=message_id,
            reply_markup=keyboards.orders.create_back_to_order_markup()
        )

        await state.clear()

    await query.answer()


@menu_router.callback_query(factories.order.slippage.filter())
async def _(
        query: CallbackQuery,
        bot: Bot,
        state: FSMContext,
        callback_data: factories.order.slippage,
):
    await st.limit_order.update(state, slippage=callback_data.slippage)

    await open_order_creation(bot, query.from_user.id, query.message.message_id, state)


async def open_order_creation(bot: Bot, user_id: int, message_id: int, state: FSMContext):
    order = await st.limit_order.get(state)

    await bot.edit_message_text(
        chat_id=user_id,
        text=texts.orders.MENU,
        message_id=message_id,
        reply_markup=keyboards.orders.create_order_creation_markup(order)
    )
