from aiogram import Router

from .starting import starting_router

menu_router = Router()

menu_router.include_routers(
    starting_router
)

__all__ = ["menu_router"]
