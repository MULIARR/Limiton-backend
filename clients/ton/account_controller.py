from pytonapi.schema.accounts import Account
from pytonapi.schema.jettons import JettonsBalances, JettonBalance
from pytonapi.async_tonapi.methods.utilites import UtilitiesMethod

from constants import TONTokenAddresses, CryptoLogo
from models.portfolio import PortfolioModel, AssetModel
from config import config


class AccountController:
    def __init__(self, tonapi):
        self.tonapi = tonapi

    async def get_portfolio(self, address: str) -> PortfolioModel:
        jettons_list = await self.get_jettons(address)

        account_data = await self.get_account(address)
        ton_balance = account_data.balance.to_amount()

        # adding TON to the assets
        jettons_list.append(
            AssetModel(
                address=TONTokenAddresses.TON,
                balance=ton_balance,
                name='Toncoin',
                symbol='TON',
                image=CryptoLogo.TON
            )
        )

        jettons_list = await self._get_rates_for_jettons_list(jettons_list)

        total_balance = sum(jetton.balance_in_usd for jetton in jettons_list)
        interface = account_data.interfaces[0] if account_data.interfaces else 'Undefined'

        account_status = account_data.status

        if True: # account_status != 'active':
            # NOTE: non-bounceable address is needed for contracts where it is important that the
            # transaction be completed regardless of whether the recipient can accept it.

            # TODO: [extra high priority] kill all stupid coders from tonapi, useless trash
            utility = UtilitiesMethod(api_key=config.tonapi.key)

            account = await utility.parse_address(address)
            address = account.non_bounceable.b64

        return PortfolioModel(
            address=address,
            total_balance=total_balance,
            wallet_interface=interface,
            status=account_status,
            assets=jettons_list
        )

    async def _get_rates_for_jettons_list(self, jettons_list: list[AssetModel]) -> list[AssetModel]:

        jettons_addresses = [jetton.address for jetton in jettons_list]

        rates_response = await self.tonapi.rates.get_prices(jettons_addresses, ['USD'])
        rates_dict = rates_response.rates

        for jetton in jettons_list:
            jetton.diff_24h = rates_dict[jetton.address]['diff_24h']['USD']

            jetton_price_in_usd = float(rates_dict[jetton.address]['prices']['USD'])
            jetton.price = jetton_price_in_usd

            jetton.balance_in_usd = jetton_price_in_usd * jetton.balance

        return jettons_list

    async def get_jettons(self, address: str) -> list[AssetModel]:
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
                    AssetModel(
                        address=jetton_user_friendly_address,
                        balance=balance,
                        name=jetton.jetton.name,
                        symbol=jetton.jetton.symbol,
                        verification=jetton.jetton.verification,
                        image=jetton.jetton.image
                    )
                )

        return jettons_list

    async def get_account(self, address: str) -> Account:
        return await self.tonapi.accounts.get_info(account_id=address)
