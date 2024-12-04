from aiogram.filters.callback_data import CallbackData


class OrderSlippageCallbackData(CallbackData, prefix='order_slippage'):
    slippage: int
