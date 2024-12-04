from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from bot import bot, dp
from clients import ton
from config import config
from database.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # TODO: remove in prod
    await db.async_init()

    await ton.async_init(bot)
    await ton.setup_limit_orders()

    await bot.set_webhook(
        url=f"{config.app.server_url}/webhook",
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info("Webhook configured")

    yield

    await bot.delete_webhook(drop_pending_updates=True)
    await ton.close()
    await db.close()
