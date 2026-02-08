from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from sqlalchemy import select

from bot.database import async_session
from bot.models import Order
from bot.handlers.order_states import OrderContactFSM

router = Router()


@router.message(OrderContactFSM.waiting_contact_phone)
async def process_contact_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    data = await state.get_data()
    order_id = data["order_id"]

    async with async_session() as session:
        order = await session.scalar(
            select(Order).where(Order.order_id == order_id)
        )

        if not order:
            await message.answer("❌ Замовлення не знайдено")
            return

        order.contact_phone = phone
        await session.commit()

    payment_link = "https://pay.pb.ua/ВАША_ПОСТОЯННАЯ_ССЫЛКА"

    await message.answer(
        f"✅ Контакт збережено\n\n"
        f"🧾 Замовлення №{order_id}\n"
        f"💰 Сума: {order.total_price} грн\n\n"
        f"💳 Посилання для оплати наразі у розробці:\n"
        f"{payment_link}\n\n"
        f"<b>Реквізити для оплати:</b>\n\n"
        f"Одержувач:\n"
        f"<pre>ФОП Дедеченко Віталій Юрійович</pre>\n"
        f"IBAN:\n"
        f"<pre>UA203052990000026008050556554</pre>\n"
        f"ЄДРПОУ:\n"
        f"<pre>3017409530</pre>\n"
        f"Банк: АТ КБ ПРИВАТБАНК\n\n"
        f"📌 Призначення платежу:\n"
        f"<pre>Оплата за замовлення №{order_id}</pre>\n"
        f"<pre>Телефон: {phone}</pre>",
        parse_mode=ParseMode.HTML
    )

    await state.clear()





