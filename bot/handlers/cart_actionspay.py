from aiogram import Router
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete

from bot.database import async_session
from bot.models import Cart, CartProduct, Order, AnnaCos

from aiogram.fsm.context import FSMContext
from bot.handlers.order_states import OrderContactFSM




router = Router()


# 💳 ОПЛАТИТИ

#1️⃣ Импортируем модель AnnaCos

from bot.models import AnnaCos




# # ниже логика и номер и ссылка на оплату сразу
@router.callback_query(lambda c: c.data == "pay")
async def pay_cart(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id

    async with async_session() as session:
        cart = await session.scalar(
            select(Cart).where(Cart.tg_id == tg_id)
        )

        if not cart or cart.total_products == 0:
            await callback.answer("🛒 Кошик порожній", show_alert=True)
            return

        products = (await session.execute(
            select(CartProduct).where(CartProduct.cart_id == cart.cart_id)
        )).scalars().all()

        products_names = ", ".join(
            f"{p.product_name} × {p.quantity}" for p in products
        )

        user = await session.scalar(
            select(AnnaCos).where(AnnaCos.tg_id == tg_id)
        )

        if not user:
            await callback.answer(
                "❌ Спочатку поділіться номером телефону",
                show_alert=True
            )
            return

        order = Order(
            client_id=user.client_id,
            client_name=user.client_name,
            tg_id=tg_id,
            phone=user.phone,
            contact_phone=user.phone,  # временно
            products_name=products_names,
            total_price=cart.total_price,
            status="pending"
        )

        session.add(order)
        await session.flush()

        order_id = order.order_id

        await session.execute(
            delete(CartProduct).where(CartProduct.cart_id == cart.cart_id)
        )
        cart.total_products = 0
        cart.total_price = 0

        await session.commit()

    # ✅ ЗАПУСК FSM
    await state.update_data(order_id=order_id)
    await state.set_state(OrderContactFSM.waiting_contact_phone)

   
    # 💳 Постоянная ссылка на оплату (ваша ссылка из Privat24)
    payment_link = "https://pay.pb.ua/ВАША_ПОСТОЯННАЯ_ССЫЛКА"

    await callback.message.answer(
    f"🧾 Дякуємо! Ваше замовлення №{order_id}\n\n"
    "📞 Вкажіть контактний номер телефону, призвище, ім'я по батькові, місто та відділення нової пошти\n"
    "Якщо номер такий самий, як у телеграм профілі — введіть його ще раз\n\n"
    #f"💳 Для оплати перейдіть за посиланням:\n{payment_link}\n\n"
    #f"У призначенні платежу укажіть: оплата за товар за замовлення №{order_id} "
    #"та укажіть ваш номер телефону\n\n"
    #"Укажить сумму замовлення яка у кошику\n"
    )
     
    

@router.callback_query(lambda c: c.data == "reserve")
async def reserve_cart(callback: CallbackQuery, state: FSMContext):
    tg_id = callback.from_user.id

    async with async_session() as session:
        # 🛒 Корзина
        cart = await session.scalar(
            select(Cart).where(Cart.tg_id == tg_id)
        )

        if not cart or cart.total_products == 0:
            await callback.answer("🛒 Кошик порожній", show_alert=True)
            return

        # 📦 Товары
        products = (await session.execute(
            select(CartProduct).where(CartProduct.cart_id == cart.cart_id)
        )).scalars().all()

        products_names = ", ".join(
            f"{p.product_name} × {p.quantity}" for p in products
        )

        # 👤 Пользователь
        user = await session.scalar(
            select(AnnaCos).where(AnnaCos.tg_id == tg_id)
        )

        if not user:
            await callback.answer(
                "❌ Спочатку поділіться номером телефону",
                show_alert=True
            )
            return

        # 🧾 Заказ
        order = Order(
            client_id=user.client_id,
            client_name=user.client_name,
            tg_id=tg_id,
            phone=user.phone,
            contact_phone=user.phone,  # временно
            products_name=products_names,
            total_price=cart.total_price,
            status="reserve"
        )

        session.add(order)
        await session.flush()           # ← ОБЯЗАТЕЛЬНО
        order_id = order.order_id       # ← ТЕПЕРЬ ЕСТЬ

        # 🧹 Чистим корзину
        await session.execute(
            delete(CartProduct).where(CartProduct.cart_id == cart.cart_id)
        )
        cart.total_products = 0
        cart.total_price = 0

        await session.commit()

    # ✅ ЗАПУСК FSM
    await state.update_data(order_id=order_id)
    await state.set_state(OrderContactFSM.waiting_contact_phone)

    
    # 💳 Постоянная ссылка на оплату (ваша ссылка из Privat24)
    payment_link = "https://pay.pb.ua/ВАША_ПОСТОЯННАЯ_ССЫЛКА"

    await callback.message.answer(
        f"🧾 Дякуємо! Ваше замовлення №{order_id} зарезервовано на 24 години\n\n"
        "📞 Вкажіть контактний номер телефону\n"
        "Якщо він такий самий — введіть його ще раз\n\n"

        "А При сплаті  замовлення вкажіть ще місто, призвище, ім'я по батькові,номер відділення нової пошти\n"   
        "У призначенні платежу вкажіть оплата за замовлення та номер замовлення \n"
        #f"💳 Для оплати перейдіть за посиланням:\n{payment_link}"
        #f"У призначенні платежу укажіть: оплата за товар за замовлення №{order_id} "
        #"Укажить сумму замовлення яка у кошику\n\n"
        #"та укажіть ваш номер телефону."

    )

    await callback.answer()


# ❌ СКАСУВАТИ
@router.callback_query(lambda c: c.data == "cancel")
async def cancel_cart(callback: CallbackQuery):
    tg_id = callback.from_user.id

    async with async_session() as session:
        cart = await session.scalar(
            select(Cart).where(Cart.tg_id == tg_id)
        )

        if cart:
            await session.execute(
                delete(CartProduct).where(CartProduct.cart_id == cart.cart_id)
            )
            cart.total_products = 0
            cart.total_price = 0
            await session.commit()

    await callback.message.answer("❌ Замовлення скасовано. Кошик очищено.")
    await callback.answer()






