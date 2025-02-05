from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, InputMedia, InputMediaPhoto

from database import db
from keyboards import ikb_select_wish
from keyboards.callback_data import CallBackData
import settings

callback_router = Router()


@callback_router.callback_query(CallBackData.filter(F.button == 'navigate'))
async def select_month(callback: CallbackQuery, callback_data: CallBackData, bot: Bot):
    target_user_id = callback_data.user_tg_id
    user_wishes = db.get_wishes(target_user_id)
    cur_id = callback_data.current_id
    *_, description, photo, url = user_wishes[cur_id]
    description = f'{cur_id+1}/{len(user_wishes)}\n' + (description or '')
    photo = photo or settings.main_photo_id
    if url:
        description += f'\n\n{url}'
    await bot.edit_message_media(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        media=InputMediaPhoto(
            media=photo,
            caption=description,
        ),
        reply_markup=ikb_select_wish(
            user_tg_id=target_user_id,
            wishlist=user_wishes,
            current_id=cur_id,
        )
    )
