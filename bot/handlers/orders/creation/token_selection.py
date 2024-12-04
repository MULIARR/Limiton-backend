from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.orders.creation.menu import open_order_creation
from bot.storages import storages as st
from bot.keyboards import keyboards
from bot.states.order import PasteCAState
from bot.texts import texts
from clients import ton

token_selection_router = Router()


@token_selection_router.message(PasteCAState.paste, F.text)
async def _(
        message: Message,
        state: FSMContext,
        bot: Bot
):
    await message.delete()

    user_id = message.from_user.id
    ca = message.text

    order = await st.limit_order.get(state)
    jetton = await ton.jettons.get_jetton(ca)

    if jetton:
        token_data = {
            "symbol": jetton.symbol,
            "address": jetton.address,
            "decimals": jetton.decimals
        }

        if order.setting_up_send_token:
            kwargs = {
                "send_token": token_data
            }

            if order.receive_token and order.receive_token.address == jetton.address:
                # if receive jetton address and send jetton address are same -> remove receive jetton data
                kwargs["receive_token"] = None
            else:
                if order.receive_token:
                    # both of tokens are configured, check pool existence and get rates
                    [send_asset, _], pool = await ton.dedust.get_pool_and_assets(
                        jetton.address, order.receive_token.address
                    )

                    is_pool_exist = await ton.dedust.check_pool_exists(pool)

                    if is_pool_exist:
                        # liquidity pool exist -> estimate swap amount and update receive token amount
                        estimated_swap_amount = await ton.dedust.estimate_swap(
                            send_asset, order.send_token.amount, jetton.decimals, order.receive_token.decimals, pool
                        )

                        kwargs["receive_token"] = {"amount": round(estimated_swap_amount, 2)}
                        kwargs["warning"] = None
                    else:
                        kwargs["receive_token"] = {"amount": 0}
                        kwargs["warning"] = None if is_pool_exist else "Liquidity pool not found"

            await st.limit_order.update(state, **kwargs)
        else:
            kwargs = {
                "receive_token": token_data
            }

            if order.send_token.address == jetton.address:
                # if receive jetton address and send jetton address are same -> remove receive jetton data
                kwargs["receive_token"] = None
                kwargs["warning"] = "Select Receive Token"
            else:
                # both of tokens are configured, check pool existence and get rates
                [send_asset, _], pool = await ton.dedust.get_pool_and_assets(
                    order.send_token.address, jetton.address
                )

                is_pool_exist = await ton.dedust.check_pool_exists(pool)

                if is_pool_exist:
                    # liquidity pool exist -> estimate swap amount and update receive token amount
                    estimated_swap_amount = await ton.dedust.estimate_swap(
                        send_asset, order.send_token.amount, order.send_token.decimals, jetton.decimals, pool
                    )

                    token_data["amount"] = round(estimated_swap_amount, 2)
                    kwargs["warning"] = None
                else:
                    token_data["amount"] = 0
                    kwargs["warning"] = "Liquidity pool not found"

            await st.limit_order.update(state, **kwargs)

        await open_order_creation(bot, user_id, order.message_id, state)

        # get out of the state
        await state.set_state(state=None)
        return True

    await bot.edit_message_text(
        chat_id=user_id,
        text=texts.orders.TOKEN_NOT_FOUND,
        message_id=order.message_id,
        reply_markup=keyboards.orders.create_back_to_order_markup()
    )
