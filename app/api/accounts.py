from fastapi import APIRouter, Request

from app.tg_init_data_auth import get_init_data_from_request
from clients import ton

accounts_router = APIRouter(
    prefix="/account"
)


@accounts_router.get("/portfolio/{address}")
async def get_portfolio(address: str, request: Request):
    """

    :param address:
    :param request:
    :return:
    """
    init_data = get_init_data_from_request(request)
    print(init_data)

    return await ton.accounts.get_portfolio(address)


@accounts_router.get("/{address}")
async def portfolio(address: str):
    """

    :param address:
    :return:
    """

    return await ton.accounts.get_account(address)
