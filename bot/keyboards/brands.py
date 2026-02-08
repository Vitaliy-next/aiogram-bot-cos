
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import text
from bot.settings import get_setting
from bot.database import async_session


async def brands_menu():
    keyboard = [
        # ─── СТАТИКА (ВСЕГДА ЕСТЬ) ───
        [
            InlineKeyboardButton(
                text=await get_setting("btn_new1", "Новінки"),
                callback_data="new_pos"
            ),
            InlineKeyboardButton(
                text=await get_setting("btn_new2", "Акції та пропозиції"),
                callback_data="Aktsii"
            ),
        ],
        [
            InlineKeyboardButton(
                text=await get_setting("btn_new3", "Прихід товару"),
                callback_data="prihod"
            ),
            InlineKeyboardButton(
                text=await get_setting("btn_new4", "Зміни цін"),
                callback_data="change_prise"
            ),
        ],
        [
            InlineKeyboardButton(
                text=await get_setting("btn_new5", "Важливі події"),
                callback_data="podii"
            ),
            InlineKeyboardButton(
                text=await get_setting("btn_new6", "Асортимент"),
                callback_data="products"
            ),
        ],
        [
            InlineKeyboardButton(
                text=await get_setting("btn_new7", "Купуй online тут"),
                callback_data="shop"
            )
        ],
    ]

    # ─── ДИНАМИКА ИЗ БД ───
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT
                    replace(key, '_text', '') AS base_key,
                    value
                FROM settings
                WHERE key LIKE 'brand%_text'
                ORDER BY key
            """)
        )
        rows = result.fetchall()

    for base_key, text_value in rows:
        keyboard.append([
            InlineKeyboardButton(
                text=text_value,
                callback_data=f"brand:{base_key}"
            )
        ])

    # ─── НАЗАД ───
    keyboard.append([
        InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data="back_to_start"
        )
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

