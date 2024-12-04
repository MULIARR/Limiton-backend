from aiogram import Router

from .importing import importing_router
from .menu import menu_router

wallet_router = Router()

wallet_router.include_routers(
    menu_router,
    importing_router
)

__all__ = ["wallet_router"]
