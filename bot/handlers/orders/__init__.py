from aiogram import Router

from .creation import creation_router
from .view import view_router

orders_router = Router()

orders_router.include_routers(
    creation_router,
    view_router
)

__all__ = ["orders_router"]
