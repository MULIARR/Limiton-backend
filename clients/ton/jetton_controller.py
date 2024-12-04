from typing import Any

from pytonapi import AsyncTonapi
from pytonapi.exceptions import TONAPIBadRequestError
from pytonapi.schema.accounts import Account
from pytonapi.schema.jettons import JettonsBalances, JettonBalance, JettonMetadata

from constants import TONTokenAddresses, CryptoLogo
from models.jettons import JettonModel, JettonsModel
from models.rates import SwapRates
from utils.format_percentage import format_percentage


class JettonController:
    def __init__(self, tonapi):
        self.tonapi: AsyncTonapi = tonapi

    async def get_jettons(self, address: str) -> JettonsModel:
        jettons_list = await self.get_jettons_data(address)

        account_data = await self.get_account_data(address)
        ton_balance = int(account_data.balance.to_amount())

        # adding TON to the assets
        jettons_list.append(
            JettonModel(
                address=TONTokenAddresses.TON,
                balance=ton_balance,
                name='Toncoin',
                symbol='TON',
                decimals=9,
                image=CryptoLogo.TON
            )
        )

        jettons_list = await self.get_rates_for_jettons(jettons_list)

        return JettonsModel(jettons=jettons_list)

    async def get_jetton(self, address: str) -> JettonModel:
        # TODO: [low priority] cheat (bad practice)
        if address == TONTokenAddresses.TON.value:
            return JettonModel(
                address=TONTokenAddresses.TON,
                balance=0,
                name='Toncoin',
                symbol='TON',
                decimals=9,
                image=CryptoLogo.TON
            )

        try:
            jetton = await self.tonapi.jettons.get_info(address)
            return JettonModel(
                address=address,
                symbol=jetton.metadata.symbol,
                name=jetton.metadata.name,
                image=jetton.metadata.image,
                verification=jetton.verification,
                decimals=jetton.metadata.decimals
            )
        except TONAPIBadRequestError:
            return False

    async def get_jetton_metadata(self, address) -> JettonMetadata:
        jetton_metadata = (await self.tonapi.jettons.get_info(address)).metadata
        return jetton_metadata

    async def get_rates_for_jettons(self, jettons_list: list[JettonModel]) -> list[JettonModel]:

        jettons_addresses = [jetton.address for jetton in jettons_list]

        rates_response = await self.tonapi.rates.get_prices(jettons_addresses, ['USD'])
        rates_dict = rates_response.rates

        for jetton in jettons_list:
            jetton_price_in_usd = float(rates_dict[jetton.address]['prices']['USD'])
            jetton.balance_in_usd = jetton_price_in_usd * jetton.balance

        return jettons_list

    async def get_rates_for_swap(self, jettons_list: list[dict[str, Any]]) -> SwapRates:
        addresses = [jetton["address"] for jetton in jettons_list]
        rates_response = await self.tonapi.rates.get_prices(addresses, ['USD'])
        rates_dict = rates_response.rates

        send_rate_in_usd = float(rates_dict[jettons_list[0]["address"]]['prices']['USD']) * jettons_list[0]["amount"]
        receive_rate_in_usd = (
                    float(rates_dict[jettons_list[1]["address"]]['prices']['USD']) * jettons_list[1]["amount"]) if len(
            jettons_list) > 1 else 0.0

        if receive_rate_in_usd:
            profit_in_usd = receive_rate_in_usd - send_rate_in_usd
            profit_percentage = (profit_in_usd / send_rate_in_usd) * 100
            profit = format_percentage(profit_percentage)
        else:
            profit = "0.00%"
            profit_percentage = 0
            profit_in_usd = 0

        return SwapRates(
            send_amount_rate_in_usd=round(send_rate_in_usd, 2),
            receive_amount_rate_in_usd=round(receive_rate_in_usd, 2),
            profit_percent=profit_percentage,
            profit_in_usd=round(profit_in_usd, 2),
            profit=profit
        )

    async def get_jettons_data(self, address: str) -> list[JettonModel]:
        jettons_data: JettonsBalances = (
            await self.tonapi.accounts.get_jettons_balances(
                account_id=address
            )
        ).balances

        jettons_list = []

        for jetton in jettons_data:
            jetton: JettonBalance

            jetton_user_friendly_address = jetton.jetton.address.to_userfriendly(is_bounceable=True)
            balance = int(jetton.balance) / pow(10, jetton.jetton.decimals)

            if balance > 0:
                jettons_list.append(
                    JettonModel(
                        address=jetton_user_friendly_address,
                        balance=balance,
                        name=jetton.jetton.name,
                        symbol=jetton.jetton.symbol,
                        decimals=jetton.jetton.decimals,
                        image=jetton.jetton.image,
                    )
                )

        return jettons_list

    async def get_account_data(self, address: str) -> Account:
        return await self.tonapi.accounts.get_info(account_id=address)
