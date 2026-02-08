from aiogram import Router
from aiogram.types import CallbackQuery

from bot.keyboards.about import about_menu

router = Router()


@router.callback_query(lambda c: c.data == "about")
async def about_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
           "ℹ️ <b>Про нас</b>\n\n"
           "Annacos_ — простір елітної косметики світових брендів 💎\n"
           "Тільки перевірені формули, інноваційні технології та видимий результат.\n\n"

           "💎 Ataché — інтенсивне відновлення та ліфтинг\n"
           "💎 Utsukusy — інноваційні формули, екзосоми та омолодження\n"
           "💎 Photozyme — захист ДНК шкіри та anti-age нового покоління\n"
           "💎 Allies of Skin — багатофункціональний догляд з клінічним ефектом\n"
           "💎 Rejudicare — глибоке відновлення, сяйво та рівний тон\n"
           "💎 Dermalogica — професійний баланс, здоров’я та комфорт шкіри\n\n"

           "Обирайте преміальний догляд для краси та молодості вашої шкіри ✨"


        ),
        reply_markup=about_menu()
    )
    await callback.answer()
# ===== КНОПКА "ВИДЕО" =====
@router.callback_query(lambda c: c.data == "about_video")
async def about_video_handler(callback: CallbackQuery):
    await callback.message.answer_video(
        video="https://t.me/annacos12/22"
    )
    await callback.answer()



