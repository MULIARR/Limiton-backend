from fastapi import APIRouter

from clients import ton

accounts_router = APIRouter(
    prefix="/accounts"
)


@accounts_router.get("/portfolio/{address}")
async def get_portfolio(address: str):
    """

    :param address:
    :return:
    """

    return await ton.accounts.get_portfolio(address)


@accounts_router.get("/{address}")
async def portfolio(address: str):
    """

    :param address:
    :return:
    """

    return await ton.accounts.get_account(address)
