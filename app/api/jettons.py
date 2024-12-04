from typing import Union, Optional

from fastapi import APIRouter, Query

from clients import ton
from models.rates import SwapRates

jettons_router = APIRouter(
    prefix="/jettons"
)


@jettons_router.get("/{address}/all")
async def jettons(address: str):
    """
    Endpoint to get a list of tokens of the selected account

    :param address:
    :return:
    """
    jettons = (await ton.jettons.get_jettons(address)).jettons

    return jettons


@jettons_router.get("/jetton/{address}")
async def jettons(address: str):
    """
    Endpoint to get information on a specific token

    :param address:
    :return:
    """
    jetton = await ton.jettons.get_jetton(address)

    return jetton


@jettons_router.get("/get_rates", response_model=SwapRates)
async def get_rates(
        send_asset_address: str = Query(..., alias="send_asset_address"),
        send_asset_amount: Union[int, float] = Query(..., alias="send_asset_amount"),
        receive_asset_address: Optional[str] = Query(None, alias="receive_asset_address"),
        receive_asset_amount: Optional[Union[int, float]] = Query(None, alias="receive_asset_amount")
) -> SwapRates:
    """
    Endpoint to get rates for swap assets

    :param send_asset_address:
    :param send_asset_amount:
    :param receive_asset_address:
    :param receive_asset_amount:
    :return:
    """
    swap_assets = [{"address": send_asset_address, "amount": send_asset_amount}]

    if receive_asset_address and receive_asset_amount is not None:
        swap_assets.append({"address": receive_asset_address, "amount": receive_asset_amount})

    return await ton.jettons.get_rates_for_swap(swap_assets)
