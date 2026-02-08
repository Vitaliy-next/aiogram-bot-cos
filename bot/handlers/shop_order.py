from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select

from bot.database import async_session
from bot.models import Product
from bot.keyboards.order_builder import products_keyboard

from bot.keyboards.shop_online import shop_menu
from bot.keyboards.brands_detail import brand_back_menu

router = Router()


@router.message(Command("order"))
async def order_start(message: Message):
    async with async_session() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()

    if not products:
        await message.answer("❌ Немає товарів для замовлення")
        return
    
    await message.answer(
    "🛒 Оберіть товар та натисніть /cart щоб перейти до кошику \n"
    " для перегляду замовлення",
    reply_markup=products_keyboard(products)
    )

# 👇 ДОБАВЛЯЕМ МЕНЮ
    await message.answer(
        "Меню магазину:",       
        reply_markup=brand_back_menu()


    )







