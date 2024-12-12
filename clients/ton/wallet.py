import logging
from pathlib import Path

import requests
from pydantic import BaseModel
from pytonlib import TonlibClient
from tonsdk.contract.wallet import Wallets, WalletVersionEnum, WalletContract
from tonsdk.crypto.exceptions import InvalidMnemonicsError
from tonsdk.utils import Address

logger = logging.getLogger(__name__)


class TonWalletModel(BaseModel):
    address: str
    address_model: Address
    mnemonics: list[str]
    public_key: bytes
    private_key: bytes
    wallet: WalletContract

    class Config:
        arbitrary_types_allowed = True


class WalletManager:
    def __init__(self):
        url_config = 'https://ton.org/global-config.json'
        config = requests.get(url_config).json()

        keystore_dir = '/tmp/ton_keystore'
        Path(keystore_dir).mkdir(parents=True, exist_ok=True)

        self.client = TonlibClient(ls_index=0, config=config, keystore=keystore_dir)

    async def init_client(self):
        await self.client.init()

    @staticmethod
    def create_wallet(
            version=WalletVersionEnum.v4r2,
            workchain=0
    ):
        mnemonics, public_key, private_key, wallet = Wallets.create(
            version=version,
            workchain=workchain
        )

        # get user-friendly wallet address
        # Initially, the address must be without a parameter (is_bounceable) so that it can receive tokens
        # but at this point it's not necessary
        user_friendly_address = wallet.address.to_string(True, True)

        return mnemonics

        # return TonWalletModel(
        #     address=user_friendly_address,
        #     address_model=wallet.address,
        #     shorten_address=get_shorten_address(user_friendly_address),
        #     mnemonics=mnemonics,
        #     public_key=public_key,
        #     private_key=private_key,
        #     wallet=wallet
        # )

    @staticmethod
    def get_wallet(
            mnemonics: list[str],
            version=WalletVersionEnum.v4r2,
            workchain=0
    ) -> TonWalletModel:
        try:
            mnemonics, public_key, private_key, wallet = Wallets.from_mnemonics(
                mnemonics=mnemonics,
                version=version,
                workchain=workchain
            )
        except InvalidMnemonicsError:
            return False

        # get user friendly wallet address
        user_friendly_address = wallet.address.to_string(True, True, True)  # bounceable

        return TonWalletModel(
            address=user_friendly_address,
            address_model=wallet.address,
            mnemonics=mnemonics,
            public_key=public_key,
            private_key=private_key,
            wallet=wallet
        )
