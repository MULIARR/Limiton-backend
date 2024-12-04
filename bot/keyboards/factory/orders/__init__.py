from .cancellation import OrderCancellationCallbackData
from .creation import OrderCreationCallbackData
from .slippage import OrderSlippageCallbackData
from .view import ViewOrderCallbackData


class OrderFactories:
    def __init__(self):
        self.creation_factory = OrderCreationCallbackData
        self.slippage_factory = OrderSlippageCallbackData
        self.view_factory = ViewOrderCallbackData
        self.cancellation_factory = OrderCancellationCallbackData

    @property
    def creation(self):
        return self.creation_factory

    @property
    def cancellation(self):
        return self.cancellation_factory

    @property
    def view(self):
        return self.view_factory

    @property
    def slippage(self):
        return self.slippage_factory


order_factories = OrderFactories()

__all__ = ['order_factories']
