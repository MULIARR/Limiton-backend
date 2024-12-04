from .log import LogTexts
from .menu import MenuTexts
from .orders import OrdersTexts
from .wallet import WalletTexts


class Texts:
    def __init__(self):
        self.menu_texts = MenuTexts()
        self.log_texts = LogTexts()
        self.wallet_texts = WalletTexts()
        self.orders_texts = OrdersTexts()

    @property
    def menu(self):
        return self.menu_texts

    @property
    def orders(self):
        return self.orders_texts

    @property
    def wallet(self):
        return self.wallet_texts

    @property
    def log(self):
        return self.log_texts


texts = Texts()

__all__ = ["texts"]
