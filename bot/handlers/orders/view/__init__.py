from aiogram import Router

from .menu import menu_router
from .specific import specific_router
from .cancellation import cancellation_router

view_router = Router()

view_router.include_routers(
    menu_router,
    specific_router,
    cancellation_router
)

__all__ = ["view_router"]
