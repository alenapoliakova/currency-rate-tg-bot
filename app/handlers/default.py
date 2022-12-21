from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.markdown import text, bold

router = Router()
start_msg = text(f"Привет! Бот делится с вами курсом валют с сайта ЦБ.\n\nОтправьте",
                 bold("/currency"), "чтобы выбрать валюту.")


@router.message(Command("start"))
async def process_start(msg: types.Message):
    await msg.answer(start_msg)


@router.message(Command("help"))
async def process_help_command(msg: types.Message):
    await msg.answer("need help")


@router.message(Command("commands"))
async def echo_handler(msg: types.Message) -> None:
    await msg.reply("Доступные команды бота:\n\n"
                    "/start - начать диалог с ботом\n"
                    "/currency - курс валют")
