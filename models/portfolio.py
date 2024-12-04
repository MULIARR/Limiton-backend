from typing import Union, Optional

from pydantic import BaseModel
from pytonapi.schema.jettons import JettonVerificationType


class AssetModel(BaseModel):
    address: str
    price: Optional[Union[int, float]] = None
    diff_24h: Optional[str] = None
    balance: Union[int, float]
    balance_in_usd: Optional[Union[int, float]] = None
    verification: JettonVerificationType = JettonVerificationType.whitelist
    name: str
    symbol: str
    image: str

    def validate_and_round(self):
        if isinstance(self.balance, float):
            self.balance = round(self.balance, 2)
        if isinstance(self.price, float):
            self.price = round(self.price, 2)
        if isinstance(self.balance_in_usd, float):
            self.balance_in_usd = round(self.balance_in_usd, 2)


class PortfolioModel(BaseModel):
    address: str
    shorten_address: Optional[str] = None
    total_balance: Union[int, float]
    wallet_interface: str
    status: str
    assets: list[AssetModel]

    def __init__(self, **kwargs):
        """
        autovalidate model
        :param kwargs
        """
        super().__init__(**kwargs)
        self.sort_assets_by_balance_in_usd()
        self.validate_balance()
        self.validate_assets()
        self.get_shorten_address()

    def get_shorten_address(self, front_chars=4, back_chars=4, ellipsis_='…') -> str:
        """
        Returns:
        str: The shortened address.
        """
        self.shorten_address = self.address[:front_chars] + ellipsis_ + self.address[-back_chars:]

    def sort_assets_by_balance_in_usd(self):
        self.assets.sort(
            key=lambda asset: asset.balance_in_usd if asset.balance_in_usd is not None else 0,
            reverse=True
        )

        ton_asset = next((asset for asset in self.assets if asset.symbol == 'TON'), None)
        usdt_asset = next((asset for asset in self.assets if asset.symbol == 'USD₮'), None)

        if ton_asset:
            self.assets.remove(ton_asset)
            self.assets.insert(0, ton_asset)
        if usdt_asset:
            self.assets.remove(usdt_asset)
            self.assets.insert(1, usdt_asset)

    def validate_balance(self):
        if isinstance(self.total_balance, float):
            self.total_balance = round(self.total_balance, 2)

    def validate_assets(self):
        for asset in self.assets:
            asset.validate_and_round()
