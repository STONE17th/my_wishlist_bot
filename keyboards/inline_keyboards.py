from aiogram.utils.keyboard import InlineKeyboardBuilder

from .callback_data import CallBackData


# from classes import Month, Day, Task
# from data_base import DataBase
# from .callback_data import CallBackData


def ikb_select_wish(user_tg_id: int, wishlist: list[tuple], current_id: int):
    keyboard = InlineKeyboardBuilder()
    target_user_id = wishlist[current_id][1]
    prev_id = (current_id - 1) % len(wishlist)
    next_id = (current_id + 1) % len(wishlist)
    keyboard.button(
        text='<<<',
        callback_data=CallBackData(
            button='navigate',
            user_tg_id=target_user_id,
            current_id=prev_id,

        ),
    )
    if target_user_id == user_tg_id:
        keyboard.button(
            text='EDIT',
            callback_data='0',
        )
        keyboard.button(
            text='DELETE',
            callback_data='0',
        )

    keyboard.button(
        text='>>>',
        callback_data=CallBackData(
            button='navigate',
            user_tg_id=target_user_id,
            current_id=next_id,

        ),
    )
    # keyboard.adjust(3, 3, 3, 3, 1)
    return keyboard.as_markup()
