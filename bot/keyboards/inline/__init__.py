from .menu import MenuKeyboards
from .utils import UtilsKeyboards
from .wallet import WalletKeyboards
from .orders import OrdersKeyboards


class Keyboards:
    def __init__(self):
        self.menu_keyboards = MenuKeyboards()
        self.walled_keyboards = WalletKeyboards()
        self.utils_keyboards = UtilsKeyboards()
        self.orders_keyboards = OrdersKeyboards()

    @property
    def menu(self):
        return self.menu_keyboards

    @property
    def orders(self):
        return self.orders_keyboards

    @property
    def wallet(self):
        return self.walled_keyboards

    @property
    def utils(self):
        return self.utils_keyboards


keyboards = Keyboards()
