from fastapi import APIRouter

from .jettons import jettons_router
from .pools import pools_router
from .accounts import accounts_router
from .orders import orders_router
from .user import users_router

api_router = APIRouter(
    prefix="/api"
)

api_routers_tuple = (
    orders_router,
    accounts_router,
    jettons_router,
    pools_router,
    users_router
)

for router in api_routers_tuple:
    api_router.include_router(router)

__all__ = [
    "api_router"
]
