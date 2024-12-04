from aiogram import Router

from .deletion import deletion_router

utils_router = Router()

utils_router.include_routers(
    deletion_router
)

__all__ = ["utils_router"]
