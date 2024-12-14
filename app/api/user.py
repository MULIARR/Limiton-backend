from fastapi import APIRouter
from database.db import db

users_router = APIRouter(
    prefix="/user"
)


from fastapi.responses import JSONResponse


@users_router.get("/{user_id}")
async def get_user_address(user_id: int) -> JSONResponse:
    """
    Endpoint to get user wallet address.

    :param user_id:
    :return: Wallet address
    """
    wallet = await db.ton_wallets.get_wallet_by_user_id(user_id)

    return JSONResponse(content=wallet.address)


