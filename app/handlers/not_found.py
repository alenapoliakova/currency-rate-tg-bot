from aiogram import Router, types

router = Router()


@router.message()
async def echo_handler(msg: types.Message) -> None:
    await msg.reply("Вы отправили неизвестную команду. Для просмотра доступных команд отправьте /commands")
