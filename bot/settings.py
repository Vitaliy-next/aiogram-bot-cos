from sqlalchemy import text
from bot.database import async_session


async def get_setting(key: str, default: str = "") -> str:
    async with async_session() as session:
        result = await session.execute(
            text("SELECT value FROM settings WHERE key = :key"),
            {"key": key}
        )
        row = result.fetchone()
        return row[0] if row else default


async def set_setting(key: str, value: str):
    async with async_session() as session:
        await session.execute(
            text("""
                INSERT INTO settings (key, value)
                VALUES (:key, :value)
                ON CONFLICT (key)
                DO UPDATE SET value = EXCLUDED.value
            """),
            {"key": key, "value": value}
        )
        await session.commit()

