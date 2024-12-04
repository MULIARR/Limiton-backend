from aiogram.filters.callback_data import CallbackData


class ViewOrderCallbackData(CallbackData, prefix='order_view'):
    order_id: str
