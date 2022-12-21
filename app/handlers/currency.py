from datetime import datetime

from aiogram import Router, types, F
from aiogram.filters import Text, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from app.keyboards import currency
from app.utils.date_parser import parse_date
from app.utils.redis_client import RedisRateHandler
from async_cb_rate.errors import CurrencyRateNotFoundError

from async_cb_rate.parser import get_rate
from app.settings import config

router = Router()

rate_cache = RedisRateHandler(host=config.REDIS_HOST, port=config.REDIS_PORT)


class CurrencyForm(StatesGroup):
    currency = State()
    date = State()


currency_date_msg = "Отправьте дату для поиска валюты в формате: 'день месяц год'. Пример: 30 12 2022\n\n" \
                    "Или отправьте /today для получения курса валюты на сегодня. Отправьте /cancel для отмены."
open_currency_markup_msg = "Выберите валюту:"


@router.message(State("*"), Command("cancel"))
@router.message(State("*"), Text("cancel", ignore_case=True))
async def cancel_handler(msg: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await msg.reply("Поиск курса валюты отменён", reply_markup=types.ReplyKeyboardRemove())


@router.message(Command("currency"))
async def process_currency(msg: types.Message, state: FSMContext):
    await msg.reply(open_currency_markup_msg, reply_markup=currency.keyboard)
    await state.set_state(CurrencyForm.currency)


@router.message(CurrencyForm.currency)
async def process_currency_date(msg: types.Message, state: FSMContext):
    if msg.text == "Назад":
        await state.clear()
        return
    if msg.text not in currency.button_names:
        return await msg.reply(f"Неверная валюта '{msg.text}'. {open_currency_markup_msg}",
                               reply_markup=currency.keyboard)
    await state.update_data(currency=msg.text)
    markup = types.ReplyKeyboardRemove()
    await msg.reply(currency_date_msg, reply_markup=markup)
    await state.set_state(CurrencyForm.date)


@router.message(CurrencyForm.date)
async def process_currency_data(msg: types.Message, state: FSMContext):
    if msg.text == "/today":
        await state.update_data(date=datetime.now())
    else:
        parsed_date = parse_date(actual_date=msg.text)
        if not isinstance(parsed_date, datetime):
            return await msg.reply(f"Неверный формат даты.\n\n{currency_date_msg}")
        await state.update_data(date=parsed_date)

    currency_data = await state.get_data()

    currency_code = currency.key_map[currency_data["currency"]]
    currency_date = currency_data["date"]
    if (found_currency := await rate_cache.get_currency(currency_code, date=currency_date)) is None:
        try:
            found_currency = await get_rate(code=currency_code, date=currency_date)
        except CurrencyRateNotFoundError:
            return await msg.reply(f"Неверный формат даты, возможно такой даты не существует.\n\n{currency_date_msg}")
        else:
            await rate_cache.add_currency(found_currency)
    search_date = found_currency.date

    markup = types.ReplyKeyboardRemove()
    await msg.answer(
        f"Курс *{found_currency.name}* на {search_date.day}.{search_date.month}.{search_date.year}: "
        f"{found_currency.price}",
        reply_markup=markup,
    )
    await state.clear()
