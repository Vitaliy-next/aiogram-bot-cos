from aiogram import Router
from aiogram.types import CallbackQuery
from bot.keyboards.brands_detail import brand_back_menu
from bot.keyboards.shop_online import shop_menu # импортирую кнопку и ниже обрабатываю callback


from sqlalchemy import select
from bot.database import async_session
from bot.models import Product



router = Router()

# ===== КНОПКА "Покупай " =====

@router.callback_query(lambda c: c.data == "shop")
async def shop_online(callback: CallbackQuery):
    async with async_session() as session:
        result = await session.execute(
            select(Product).limit(5)
        )
        products = result.scalars().all()

    if not products:
        await callback.message.edit_text("❌ Товари відсутні")
        await callback.answer()
        return

    text = "🛒 Доступні товари:\n\n"
    for p in products:
        text += f"• {p.product_name} — {float(p.price)} грн\n"

    text += "\n👉 Щоб купити онлайн — натисніть /order"
    
    await callback.message.edit_text(
        text,
        reply_markup=brand_back_menu() # этот хендлер работает
        
    )

    #await callback.message.edit_text(text)
    await callback.answer()



# ===== КНОПКА "Назад к брендам" =====
@router.callback_query(lambda c: c.data == "back_to_brands")
async def back_to_brands(callback: CallbackQuery):
    from bot.keyboards.brands import brands_menu

    await callback.message.edit_text(
        "🧴 Наши основні пропозиціі та цікава інформація:",
        reply_markup=brands_menu()  # возвращаем меню брендов
    )
    await callback.answer()

