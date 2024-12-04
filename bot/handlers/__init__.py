from aiogram import Router

from .menu import menu_router
from .orders import orders_router
from .wallet import wallet_router
from .utils import utils_router

main_router = Router()

main_router.include_routers(
    menu_router,
    orders_router,
    wallet_router,
    utils_router
)

__all__ = [
    "main_router"
]
