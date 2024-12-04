import asyncio
from typing import Union

from dedust import Asset, Factory, PoolType, JettonRoot, VaultJetton, SwapParams, VaultNative, Pool, JettonWallet
from dedust.contracts.dex import ReadinessStatus
from pytoniq import LiteBalancer, WalletV4R2, LiteServerError, WalletV4, RunGetMethodError
from pytoniq_core import Cell, Address

from constants import TONTokenAddresses


class DeDustController:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DeDustController, cls).__new__(cls, *args, **kwargs)
            cls._instance.provider = LiteBalancer.from_mainnet_config(2)
        return cls._instance

    def __init__(self):
        self.dedust_ton_vault = "EQDa4VOnTYlLvDJ0gZjNYm5PXfSmmtL6Vs6A_CZEtXCNICq_"  # noqa

    async def async_init(self):
        await self.provider.start_up()

    async def get_wallet_from_mnemonics(self, mnemonics: list[str]) -> WalletV4R2:
        return await WalletV4R2.from_mnemonic(
            provider=self.provider,
            mnemonics=mnemonics
        )

    async def get_pool_and_assets(
            self,
            send_jetton_address: str,
            receive_jetton_address: str,
            _max_attempts=5,
            _attempt=0
    ) -> tuple[list[Asset], Pool]:

        def get_asset(address: str) -> Asset:
            return Asset.jetton(address) if address != TONTokenAddresses.TON.value else Asset.native()

        send_jetton_asset = get_asset(send_jetton_address)
        receive_jetton_asset = get_asset(receive_jetton_address)

        # USDT/USDC, TON/stTON pools are stable
        stable_pairs = {
            (TONTokenAddresses.USDT.value, TONTokenAddresses.USDC.value),
            (TONTokenAddresses.USDC.value, TONTokenAddresses.USDT.value),
            (TONTokenAddresses.TON.value, TONTokenAddresses.stTON.value),
            (TONTokenAddresses.stTON.value, TONTokenAddresses.TON.value),
        }

        pool_type = PoolType.STABLE \
            if (send_jetton_address, receive_jetton_address) in stable_pairs else PoolType.VOLATILE

        while _attempt < _max_attempts:
            try:
                pool = await Factory.get_pool(
                    pool_type, [send_jetton_asset, receive_jetton_asset],
                    self.provider
                )
                break
            except LiteServerError as e:
                await asyncio.sleep(0.3)
                _attempt += 1
                if _attempt >= _max_attempts:
                    raise e
            except RunGetMethodError as e:
                raise e

        return [send_jetton_asset, receive_jetton_asset], pool

    async def get_send_jetton_objects(
            self,
            send_jetton_address: str,
            user_wallet: WalletV4R2
    ) -> tuple[VaultJetton, JettonWallet]:
        jetton_vault = await Factory.get_jetton_vault(send_jetton_address, self.provider)
        jetton_root: JettonRoot = JettonRoot.create_from_address(send_jetton_address)
        jetton_wallet = await jetton_root.get_wallet(user_wallet.address, self.provider)

        return jetton_vault, jetton_wallet

    @staticmethod
    def prepare_swap(
            is_ton_sending: bool,
            send_amount: Union[int, float],
            minimum_to_receive: Union[int, float],
            pool: Pool,
            jetton_vault: VaultJetton,
            jetton_wallet: JettonWallet,
            recipient_address: Address
    ) -> Cell:
        send_amount_nano = int(send_amount * 1e9)
        minimum_to_receive_nano = int(minimum_to_receive * 1e9)

        if is_ton_sending:
            swap_params = SwapParams(
                recipient_address=recipient_address
            )

            swap = VaultNative.create_swap_payload(
                limit=minimum_to_receive_nano,
                amount=send_amount_nano,
                pool_address=pool.address,
                swap_params=swap_params
            )
        else:
            swap_payload = VaultJetton.create_swap_payload(
                limit=minimum_to_receive_nano,
                pool_address=pool.address
            )

            swap = jetton_wallet.create_transfer_payload(
                destination=jetton_vault.address,
                amount=send_amount_nano,
                response_address=recipient_address,
                forward_amount=int(0.25 * 1e9),  # comm?
                forward_payload=swap_payload
            )

        return swap

    async def execute_swap(
            self,
            swap: Cell,
            send_amount: Union[int, float],
            jetton_wallet: JettonWallet,
            user_wallet: WalletV4,
            is_ton_sending: bool
    ) -> bool:
        if is_ton_sending:
            send_amount_nano = int((send_amount * 1e9) + (0.25 * 1e9))  # 0.25 = gas_value

            await user_wallet.transfer(
                destination=self.dedust_ton_vault,
                amount=send_amount_nano,
                body=swap
            )
        else:
            await user_wallet.transfer(
                destination=jetton_wallet.address,
                amount=int(0.3 * 1e9),  # gas
                body=swap
            )

        return True

    async def estimate_swap(
            self,
            send_asset: Asset,
            send_amount: Union[int, float],
            send_asset_decimals: int,
            receive_asset_decimals: int,
            pool: Pool,
            _attempt=0,
            _max_attempts=5
    ) -> Union[int, float]:
        amount_in = int(send_amount * pow(10, send_asset_decimals))

        while _attempt < _max_attempts:
            try:
                pool_answer = await pool.get_estimated_swap_out(
                    asset_in=send_asset,
                    amount_in=amount_in,
                    provider=self.provider
                )
                return pool_answer["amount_out"] / pow(10, receive_asset_decimals)
            except LiteServerError as e:
                print(e)
                await asyncio.sleep(2)
                _attempt += 1
                if _attempt >= _max_attempts:
                    return False

            return False

    async def check_pool_exists(self, pool: Pool) -> bool:
        return True if await (pool.get_readiness_status(self.provider)) == ReadinessStatus.READY else False
        # while _attempt < _max_attempts:
        #     try:
        #         return True if await (pool.get_readiness_status(self.provider)) == ReadinessStatus.READY else False
        #     except LiteServerError:
        #         await asyncio.sleep(0.3)
        #         _attempt += 1
        #         if _attempt >= _max_attempts:
        #             return False

    async def close(self):
        await self.provider.close_all()
