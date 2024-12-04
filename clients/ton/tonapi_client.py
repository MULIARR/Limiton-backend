from pytonapi import AsyncTonapi
from pytonapi.schema.accounts import Account
from pytonapi.schema.events import TransactionEventData
from pytonapi.schema.jettons import JettonInfo

from config import config
from models.jetton_metadata import JettonMetadataModel


class AsyncTONApiClient(AsyncTonapi):
    def __init__(self, tonapi_key: str):
        super().__init__(api_key=tonapi_key)

    async def get_account_info(self, address: str) -> Account:
        return await self.accounts.get_info(account_id=address)

    async def get_jetton_data(self, jetton_address: str) -> JettonInfo:
        # TODO: Redis Cache

        return await self.jettons.get_info(jetton_address)

    async def get_jetton_metadata(self, jetton_address: str) -> JettonMetadataModel:
        # TODO: Redis Cache

        jetton_metadata = (await self.jettons.get_info(jetton_address)).metadata
        return JettonMetadataModel(**jetton_metadata.dict())

    @staticmethod
    async def handler(event: TransactionEventData, tonapi: AsyncTonapi) -> None:
        """
        Handle SSEvent for transactions.

        :param event: The SSEvent object containing transaction details.
        :param tonapi: An instance of AsyncTonapi for interacting with TON API.
        """
        trace = await tonapi.traces.get_trace(event.tx_hash)

        # If the transaction is successful, print the trace
        if trace.transaction.success:
            print(trace.dict())


tonapi_client = AsyncTONApiClient(tonapi_key=config.tonapi.key)
