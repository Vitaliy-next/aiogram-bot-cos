from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from sqlalchemy import select

from bot.models import AnnaCos, Order
from bot.database import async_session
from bot.handlers.clients_states import ClientsAccess
from bot.config import CLIENTS_PASSWORD,ORDERS_PASSWORD

router = Router()

#ORDERS_PASSWORD = " "


# ───────────────────────────────
#              /clients
# ───────────────────────────────
@router.message(Command("clients"))
async def clients_entry(message: Message, state: FSMContext):
    await message.answer("🔐 Введите пароль для просмотра клиентов:")
    await state.set_state(ClientsAccess.waiting_clients_password)


@router.message(ClientsAccess.waiting_clients_password)
async def check_clients_password(message: Message, state: FSMContext):
    if message.text != CLIENTS_PASSWORD:
        await message.answer("❌ Неверный пароль.")
        await state.clear()
        return

    async with async_session() as session:
        result = await session.execute(select(AnnaCos))
        rows = result.scalars().all()

    if not rows:
        await message.answer("Таблица клиентов пустая.")
        await state.clear()
        return

    text = "📋 <b>Клиенты:</b>\n\n"

    for r in rows:
        text += (
            f"🆔 ID: {r.client_id}\n"
            f"👤 Имя: {r.client_name}\n"
            f"📞 Телефон: {r.phone}\n"
            "──────────────\n"
        )

    await message.answer(text, parse_mode="HTML")
    await state.clear()


# ───────────────────────────────
#              /orders
# ───────────────────────────────
@router.message(Command("orders"))
async def orders_entry(message: Message, state: FSMContext):
    await message.answer("🔐 Введите пароль для просмотра заказов:")
    await state.set_state(ClientsAccess.waiting_orders_password)


@router.message(ClientsAccess.waiting_orders_password)
async def check_orders_password(message: Message, state: FSMContext):
    if message.text != ORDERS_PASSWORD:
        await message.answer("❌ Неверный пароль.")
        await state.clear()
        return

    async with async_session() as session:
        result = await session.execute(select(Order))
        rows = result.scalars().all()

    if not rows:
        await message.answer("Таблица orders пустая.")
        await state.clear()
        return

    text = "📦 <b>Список заказов:</b>\n\n"

    for r in rows:
        text += (
            f"🆔 Order ID: {r.order_id}\n"
            f"👤 Клиент: {r.client_name or '—'}\n"
            f"📞 Телефон: {r.phone or '—'}\n"
            f"🛍 Товары: {r.products_name or '—'}\n"
            f"💰 Сумма: {r.total_price or 0} грн\n"
            f"📌 Статус: {r.status}\n"
            f"📅 Дата: {r.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            "────────────────────\n"
        )

    await message.answer(text, parse_mode="HTML")
    await state.clear()







