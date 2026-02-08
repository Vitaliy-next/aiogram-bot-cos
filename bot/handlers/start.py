from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    CallbackQuery
)
from aiogram.filters import Command, CommandObject
from sqlalchemy import text

from bot.database import async_session
from bot.settings import get_setting, set_setting

router = Router()


# ───────────────────────────────
#        INLINE МЕНЮ
# ───────────────────────────────

async def start_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=await get_setting("btn1", "Новінки, акції, продукція"),
                    callback_data="brands"
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_setting("btn2", "Зв'язатися з нами"),
                    callback_data="contact"
                )
            ],
            [
                InlineKeyboardButton(
                    text=await get_setting("btn3", "Про компанію GROSS"),
                    callback_data="about"
                )
            ],
            [
            InlineKeyboardButton(
                text=await get_setting("btn_new7", "Купуй online тут"),
                callback_data="shop"
            )
            ]


        ]
    )


def guest_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="➡️ Увійти без реєстрації",
                    callback_data="guest_login"
                )
            ]
        ]
    )


contact_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📱 Поділитися контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# ───────────────────────────────
#      /start
# ───────────────────────────────

@router.message(Command("start"))
async def start_cmd(message: Message):
    chat_id = message.chat.id

    async with async_session() as session:
        result = await session.execute(
            text("SELECT client_id FROM annacostest WHERE tg_id = :tg"),
            {"tg": chat_id}
        )
        client = result.fetchone()

    if not client:
        guest_text = await get_setting(
            "guest",
            "👋 Вітаю Вас в інформаційному телеграм каналі  компанії Annacos, тут ви можете ознайомитися з брендами, акціями, знижками тощо!\n"
   
            "Щоб продовжити, будь ласка, поділіться номером телефону 💎"
        )

        await message.answer(guest_text, reply_markup=contact_kb)
        await message.answer(
            "Також ви можете увійти без реєстрації:",
            reply_markup=guest_menu()
        )
        return

    registered_text = await get_setting(
        "rguest",
        "Вітаю Леді! 👋\n"
        "Я — офіційний бот компанії Annacos_\n"
        "Обирайте розділ нижче 💎"
    )

    await message.answer(registered_text, reply_markup=await start_menu())

# ───────────────────────────────
#      ОБРАБОТКА КОНТАКТА
# ───────────────────────────────

@router.message(F.contact)
async def contact_handler(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    name = message.from_user.first_name or "Telegram user"

    async with async_session() as session:
        await session.execute(
            text("""
                INSERT INTO annacostest (
                    tg_id, client_name, phone,
                    city, products, summ_sale,
                    activity, additional_info, period
                )
                VALUES (:tg, :name, :phone, NULL, NULL, 0,
                        'new', 'Добавлен через Telegram', NULL)
            """),
            {"tg": chat_id, "name": name, "phone": phone}
        )
        await session.commit()

    await message.answer(
        "✅ Дякую! Ви успішно зареєстровані 💎",
        reply_markup=ReplyKeyboardRemove()
    )
    await message.answer("Оберіть розділ:", reply_markup=await start_menu())

# ───────────────────────────────
#      ГОСТЕВОЙ ВХОД
# ───────────────────────────────
@router.callback_query(F.data == "guest_login")
async def guest_login(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    name = callback.from_user.first_name or "Telegram user"

    # сохраняем гостя
    try:
        async with async_session() as session:
            await session.execute(
                text("""
                    INSERT INTO chat_id (tg_id, name)
                    VALUES (:tg, :name)
                    ON CONFLICT (tg_id) DO NOTHING
                """),
                {
                    "tg": chat_id,
                    "name": name
                }
            )
            await session.commit()
    except Exception as e:
        print("❌ DB ERROR (guest_login):", e)

    guest_text = await get_setting(
        "guest",
        "👋 Вітаю мої Леді! в інформаційному каналі компанії annacos_!"
    )

    await callback.message.edit_text(
        guest_text + "\n\nВи зайшли без реєстрації 👀",
        reply_markup=await start_menu()
    )

    await callback.answer()



# ───────────────────────────────
#      BACK TO START
# ───────────────────────────────

@router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery):
    text = await get_setting(
        "rguest",
        "Вітаю! 👋 Оберіть розділ нижче 💎"
    )

    await callback.message.edit_text(
        text,
        reply_markup=await start_menu()
    )
    await callback.answer()













