from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import text

from bot.database import async_session
from bot.settings import get_setting


async def contact_menu() -> InlineKeyboardMarkup:
    keyboard = []

    # --- менеджеры ---
    async with async_session() as session:
        result = await session.execute(
            text("""
                SELECT key, value
                FROM settings
                WHERE key LIKE 'cont%_tg'
                ORDER BY key
            """)
        )
        managers = result.fetchall()

    for key, url in managers:
        keyboard.append([
            InlineKeyboardButton(
                text=f"✉️ Менеджер {key.replace('cont', '').replace('_tg', '')}",
                url=url
            )
        ])

    # --- стандартные кнопки ---
    site_url = await get_setting("cont_site", "https://www.instagram.com/annacos_")
    channel_url = await get_setting("cont_channel", "https://t.me/annacos12")

    keyboard.extend([
        [InlineKeyboardButton(text="🌐 Наш сайт", url=site_url)],
        [InlineKeyboardButton(text="📢 Наш канал", url=channel_url)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

