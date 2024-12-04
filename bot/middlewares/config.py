from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message

from config import Config


class ConfigMiddleware(BaseMiddleware):
    def __init__(self, config: Config, db) -> None:
        self.config = config
        self.db = db

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["config"] = self.config
        data["db"] = self.db

        return await handler(event, data)
