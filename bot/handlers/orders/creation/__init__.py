from aiogram import Router

from .amount import amount_router
from .menu import menu_router
from .slippage import slippage_router
from .token_selection import token_selection_router

creation_router = Router()

creation_router.include_routers(
    menu_router,
    slippage_router,
    token_selection_router,
    amount_router
)

__all__ = ["creation_router"]
