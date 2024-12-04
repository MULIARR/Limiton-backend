from .orders import order_factories


class Factories:
    def __init__(self):
        self.order_factories = order_factories

    @property
    def order(self):
        return self.order_factories


factories = Factories()

__all__ = ['factories']
