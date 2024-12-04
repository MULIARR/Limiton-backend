from aiogram.filters.callback_data import CallbackData


class OrderCancellationCallbackData(CallbackData, prefix='order_cancellation'):
    order_id: str
