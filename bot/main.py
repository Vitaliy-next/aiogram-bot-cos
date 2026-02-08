import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from bot.config import BOT_TOKEN
from bot.database import engine, Base
from bot.models import AnnaCos, Media


from bot.handlers.start import router as start_router
from bot.handlers.brands import router as brands_router
from bot.handlers.admin_router import router as admin_router
from bot.handlers.clients import router as clients_router
from bot.handlers.about import router as about_router
from bot.handlers.contact import router as contact_router
#from bot.handlers.shop import router as shop_router
from bot.handlers.shop_online import router as shop_router
from bot.handlers.back_to_start import router as back_router
from bot.handlers.admin_media import router as media_router
from bot.handlers.show_video  import router as show_router
from bot.handlers.newpos_video  import router as newpos_router # вот этот роутер теперь в новинках

from bot.handlers.products_video  import router as productsvid_router # вот этот роутер теперь в ассортименте
from bot.handlers.aktsii_video  import router as aktsii_router # вот этот роутер теперь в акциях
from bot.handlers.prihod_video  import router as prihod_router # вот этот роутер теперь в приходах

from bot.handlers.changeprise_video  import router as changeprise_router # вот этот роутер теперь в изм цен

from bot.handlers.cart import router as cart_router
from bot.handlers.shop_order import router as shoporder_router

from bot.handlers.cart_view import router as cart_view_router
from bot.handlers.cart_manage import router as cart_manage_router


from bot.handlers.cart_actions import router as cart_actions_router

#from bot.handlers.cart_actionspay import router as actionspay_router
from bot.handlers.cart_actionspay import router as actionspay_router


from bot.handlers.order_contact import router as ordercontact_router


from bot.handlers.admin_settings import router as settings_router


async def on_startup():
    async with engine.begin() as conn:
        # ⚠️ НЕ создаёт таблицы заново, если они уже есть
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await on_startup()

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    # ✅ FSM storage обязателен
    dp = Dispatcher(storage=MemoryStorage())

    # порядок важен: сначала клиентские, потом админ
    dp.include_router(start_router)
    dp.include_router(back_router)
    dp.include_router(shop_router)
    dp.include_router(brands_router)
    dp.include_router(clients_router)
    dp.include_router(about_router)
    dp.include_router(contact_router)
    dp.include_router(admin_router)
    dp.include_router(media_router)
    dp.include_router(show_router)
    dp.include_router(newpos_router)
    dp.include_router(productsvid_router)
    dp.include_router(aktsii_router)
    dp.include_router(prihod_router)
    dp.include_router(changeprise_router)
    dp.include_router(cart_router)
    dp.include_router(shoporder_router)
    dp.include_router(cart_view_router)
    dp.include_router(cart_manage_router)
    dp.include_router(cart_actions_router)
    #dp.include_router(actionspay_router)
    dp.include_router(actionspay_router)
    dp.include_router(ordercontact_router)
    dp.include_router(settings_router)
   

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

