from aiogram.filters.callback_data import CallbackData


class OrderCreationCallbackData(CallbackData, prefix='order_creation'):
    action: str
