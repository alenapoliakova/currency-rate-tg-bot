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
    await bot.set_webhook(
        url=config.WEBHOOK_URL,
        drop_pending_updates=True,
        allowed_updates=dp.resolve_used_update_types()
    )


@app.post("/")
async def start(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_webhook_update(bot, telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()
    await dp.storage.close()
