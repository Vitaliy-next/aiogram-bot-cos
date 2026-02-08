from aiogram import Router
from aiogram.types import Message
from sqlalchemy import select

from bot.database import async_session
from bot.models import Cart, CartProduct
from bot.keyboards.cart_manage import cart_manage_keyboard
from bot.keyboards.cart_actions import cart_actions_menu

from bot.keyboards.shop_online import shop_menu
from bot.keyboards.brands_detail import brand_back_menu
router = Router()


@router.message(lambda m: m.text == "/cart")
async def show_cart(message: Message):
    tg_id = message.from_user.id

    async with async_session() as session:
        result = await session.execute(
            select(Cart).where(Cart.tg_id == tg_id)
        )
        cart = result.scalar_one_or_none()

        if not cart or cart.total_products == 0:
            await message.answer("🛒 Ваш кошик порожній")
            return

        result = await session.execute(
            select(CartProduct).where(CartProduct.cart_id == cart.cart_id)
        )
        products = result.scalars().all()

    text = "🛒 **Ваш кошик:**\n\n"

    for p in products:
        text += (
            f"• {p.product_name}\n"
            f"  К-сть: {p.quantity}\n"
            f"  Сума: {float(p.final_price)} грн\n\n"
        )

    text += f"💰 **Разом:** {float(cart.total_price)} грн"



    # ⬇️ ВОТ СЮДА
    await message.answer(
        text,
        reply_markup=cart_manage_keyboard(products)
    )
    await message.answer(
        "Оберіть дію:",
        reply_markup= cart_actions_menu()
    )
    

    # 👇 НАВИГАЦИЯ (назад в магазин, меню и т.д.)
    await message.answer(
        "Навігація:",
        #reply_markup= shop_menu()
        reply_markup=brand_back_menu()
    )

    

    














