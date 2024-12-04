import asyncio
import logging
import os

import uvicorn
from aiogram.types import Update
from fastapi import Request

from app import app
from bot import dp, bot

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    port = int(os.environ.get("PUBLIC_PORT", 9097))
    host = str(os.environ.get("HOST", "127.0.0.1"))

    config = uvicorn.Config(app, host, port=port, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("SYSTEM OFF")

