from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from bot.settings import set_setting
from bot.config import BTN_PASSWORD
router = Router()

#BTN_PASSWORD = " "


@router.message(Command("setbtn"))
async def set_button(message: Message, command: CommandObject):
    """
    /setbtn пароль ключ текст
    """
    if not command.args:
        await message.answer(
            "Формат:\n"
            "/setbtn пароль btn_new Нове ім'я"
        )
        return

    password, key, *text = command.args.split()

    if password != BTN_PASSWORD:
        await message.answer("❌ Невірний пароль")
        return

    if not text:
        await message.answer("❗ Введіть текст кнопки")
        return

    await set_setting(key, " ".join(text))
    await message.answer(f"✅ Кнопка `{key}` оновлена")
