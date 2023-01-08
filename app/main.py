import logging
from fastapi import FastAPI
from aiogram import types, F

from app.bot import dp, bot
from app.handlers import default, currency, not_found
from app.settings import config

app = FastAPI()

dp.message.filter(F.chat.type == "private")
dp.include_router(default.router)
dp.include_router(currency.router)
dp.include_router(not_found.router)


@app.on_event("startup")
async def on_startup():
    logging.info(f"using <{config.SENDING_TYPE}> type")
    match config.SENDING_TYPE:
        case "webhook":
            await bot.set_webhook(
                url=config.WEBHOOK_URL,
                drop_pending_updates=False,
                allowed_updates=dp.resolve_used_update_types()
                )
        case "polling":
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)


@app.post("/")
async def start(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot, telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    await dp.storage.close()
