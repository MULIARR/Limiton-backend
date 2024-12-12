from typing import Union

from fastapi import APIRouter

from clients import ton

pools_router = APIRouter(
    prefix="/pool"
)


@pools_router.get("/is_exist/{send_jetton_address}/{receive_jetton_address}")
async def check_pool_exists(send_jetton_address: str, receive_jetton_address: str) -> bool:
    """
    Endpoint to check if pool exists

    :param send_jetton_address:
    :param receive_jetton_address:
    :return:
    """

    _, pool = await ton.dedust.get_pool_and_assets(
        send_jetton_address, receive_jetton_address
    )

    is_pool_exist = await ton.dedust.check_pool_exists(pool)

    return is_pool_exist


@pools_router.get("/estimate_swap_out")
async def estimate_swap_out(
        send_jetton_address: str,
        send_jetton_amount: Union[int, float],  # asset in
        send_asset_decimals: int,
        receive_jetton_address: str,
        receive_asset_decimals: int
) -> Union[int, float]:
    """

    :param send_jetton_address:
    :param send_jetton_amount:
    :param send_asset_decimals
    :param receive_jetton_address:
    :param receive_asset_decimals:
    :return:
    """

    [send_asset, _], pool = await ton.dedust.get_pool_and_assets(
        send_jetton_address, receive_jetton_address
    )

    estimated_swap_out = await ton.dedust.estimate_swap(
        send_asset, send_jetton_amount, send_asset_decimals, receive_asset_decimals, pool
    )

    return estimated_swap_out



