from typing import Optional, Union

from pydantic import BaseModel
from pytonapi.schema.jettons import JettonVerificationType


# for jettons controller


class JettonModel(BaseModel):
    address: str
    balance: Optional[Union[int, float]] = None
    balance_in_usd: Optional[Union[int, float]] = None
    symbol: str
    name: str
    image: str
    verification: JettonVerificationType = JettonVerificationType.whitelist
    decimals: int

    def validate_and_round(self):
        if isinstance(self.balance, float):
            self.balance = round(self.balance, 2)
        if isinstance(self.balance_in_usd, float):
            self.balance_in_usd = round(self.balance_in_usd, 2)


class JettonsModel(BaseModel):
    jettons: list[JettonModel]

    def __init__(self, **kwargs):
        """
        autovalidate model
        :param kwargs
        """
        super().__init__(**kwargs)
        self.sort_assets_by_balance_in_usd()
        self.validate_jettons()

    def sort_assets_by_balance_in_usd(self):
        self.jettons.sort(
            key=lambda jetton: jetton.balance_in_usd if jetton.balance_in_usd is not None else 0,
            reverse=True
        )

        ton_asset = next((jetton for jetton in self.jettons if jetton.symbol == 'TON'), None)
        usdt_asset = next((jetton for jetton in self.jettons if jetton.symbol == 'USD₮'), None)

        if ton_asset:
            self.jettons.remove(ton_asset)
            self.jettons.insert(0, ton_asset)
        if usdt_asset:
            self.jettons.remove(usdt_asset)
            self.jettons.insert(1, usdt_asset)

    def validate_jettons(self):
        for jetton in self.jettons:
            jetton.validate_and_round()
