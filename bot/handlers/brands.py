from aiogram import Router
from aiogram import F

from aiogram.types import CallbackQuery
from bot.keyboards.brands_detail import brand_back_menu
from bot.keyboards.show_video import podii_menu

from bot.keyboards.newpos_video import newpos_menu

from bot.keyboards.products_video import products_menu # это подключение клавиатуры ассортимент видео

from bot.keyboards.aktsii_video import aktsii_menu

from bot.keyboards.prihod_video import prihod_menu # это подключение клавиатуры приход видео

from bot.keyboards.changeprise_video import changeprise_menu # это подключение клавиатуры изменение цен видео


from bot.settings import get_setting


#from bot.keyboards.reply_shop import shop_reply_menu

from bot.keyboards.brands import brands_menu
from sqlalchemy import select
from bot.database import async_session
from bot.models import Media
from bot.models import InfoBlock
from bot.models import StockBlock
from bot.models import PriseBlock
from bot.models import PodiiBlock
from bot.models import ProductBlock
from bot.models import NewproductBlock



router = Router()

@router.callback_query(lambda c: c.data == "brands")
async def brands_handler(callback: CallbackQuery):
    print("🔥 CALLBACK brands triggered")

    await callback.message.edit_text(

        text="🧴 Моя леді, тут ви знайдете всі новинки, акції та приємні пропозиції ✨\n\n"
                "А про найважливіше я іноді писатиму вам особисто — з турботою та теплом 🤍",

        #text="🧴 Леді! про новинки, акції та ін. можеш дізнатися нижче, але я буду ,інколи "
             #"писати тобі про головне особисто 🔥",
        reply_markup=await brands_menu()   # ✅ ВАЖНО
    )

    await callback.answer()


@router.callback_query(F.data & F.data.startswith("brand:"))
async def brand_handler(callback: CallbackQuery):
    brand_id = callback.data.split(":", 1)[1]

    text = await get_setting(
        f"{brand_id}_reply",
        "Немає інформації"
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=brand_back_menu()  # ✅ кнопка «Назад»
    )

    await callback.answer()


# @router.callback_query(F.data & F.data.startswith("brand:"))
# async def brand_handler(callback: CallbackQuery):
#     brand_id = callback.data.split(":", 1)[1]

#     text = await get_setting(f"{brand_id}_reply", "Немає інформації")
#     await callback.message.edit_text(text)
         
        
#     await callback.answer()

# @router.callback_query(F.data.startswith("brand:"))
# async def brand_handler(callback: CallbackQuery):
#     brand_id = callback.data.split(":", 1)[1]

#     text = await get_setting(f"{brand_id}_reply", "Немає інформації")
#     await callback.message.edit_text(text)






# # ===== КНОПКА "BRANDS" =====
# @router.callback_query(lambda c: c.data == "brands")
# async def brands_handler(callback: CallbackQuery):
#     print("🔥 CALLBACK brands triggered")
#     await callback.message.edit_text(
#         text="🧴 Друже! про новинки, акції та ін. можеш дізнатися нижче, але я буду ,інколи "
#         "писати тобі про головне особисто 🔥",
#         reply_markup=brands_menu()
#     )

     

    await callback.answer()


# ===== ОБРАБОТЧИКИ БРЕНДОВ =====


# показываю обработку одного меню  новинки, в подменю появляется видео

@router.callback_query(lambda c: c.data == "new_pos")
async def newpos_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(NewproductBlock).where(NewproductBlock.code == "Newproducts")
        )
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація по новінкам відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=newpos_menu()
        
    )
    
    
    
    await callback.answer()

# показываю обработку одного меню  ассортимент, в подменю появляется видео

@router.callback_query(lambda c: c.data == "Aktsii")
async def products_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(InfoBlock).where(InfoBlock.code == "Aktsii")
        )
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація про акціі та пропозиціі відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=aktsii_menu()
        
    )
    
    
    
    await callback.answer()






# показываю обработку одного меню  ассортимент, в подменю появляется видео

@router.callback_query(lambda c: c.data == "prihod")
async def prihod_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(StockBlock).where(StockBlock.code == "Prihod")
        )
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація про приходи товару відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=prihod_menu()
        
    )
    
    
    
    await callback.answer()




# показываю обработку одного меню  изменение цен, в подменю появляется видео

@router.callback_query(lambda c: c.data == "change_prise")
async def changeprise_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(PriseBlock).where(PriseBlock.code == "Prise")
        )
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація про зміни цін відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=changeprise_menu()
        
    )
    
    
    
    await callback.answer()






@router.callback_query(lambda c: c.data == "podii")
async def podii_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(PodiiBlock).where(PodiiBlock.code == "Podii")
        )
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація по подіях відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=podii_menu()
        
    )
    
    
    
    await callback.answer()

# Раньше этот callback обрабатывался, теперь выше

# показываю обработку одного меню  ассортимент, в подменю появляется видео

@router.callback_query(lambda c: c.data == "products")
async def products_handler(callback: CallbackQuery):

    async with async_session() as session:
        result = await session.execute(
            select(ProductBlock).where(ProductBlock.code == "Products")
        )
        
        block = result.scalar_one_or_none()

    text = block.text if block else (
        "💧 Вибачте, але на зараз інформація о продукціі відсутня"
    )

    await callback.message.edit_text(
        text,
        reply_markup=products_menu()
        
    )
    
    
    
    await callback.answer()


