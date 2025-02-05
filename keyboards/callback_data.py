from aiogram.filters.callback_data import CallbackData


class CallBackData(CallbackData, prefix='WLB'):
    button: str
    user_tg_id: int = 0
    current_id: int = 0
