from typing import Optional, Union

from pydantic import BaseModel

from bot.storages.base import BaseStorage
from constants import TONTokenAddresses


class TokenModel(BaseModel):
    """
    Represents token.
    """

    symbol: str = "TON"
    address: str = TONTokenAddresses.TON.value
    amount: Union[int, float] = 5
    decimals: int = 9
    usd_rate: Union[int, float] = 0


class LimitOrderStorageModel(BaseModel):
    """
    Represents limit order configuration.

    Attributes:
    - send_token: Token to be sent, or None if unset.
    - receive_token: Token to be received, or None if unset.
    - slippage: Allowed slippage percentage.
    - minimum_to_receive: Minimum amount of receive token required.
    - setting_up_send_token: Flag indicating if configuring send token (default: True).
    - warning: Warning message
    - message_id:
    """

    send_token: Optional[TokenModel] = TokenModel()
    receive_token: Optional[TokenModel] = None
    slippage: Optional[int] = 2
    minimum_to_receive: Optional[Union[int, float]] = None
    setting_up_send_token: bool = True
    warning: Optional[str] = "Select Receive Token"
    message_id: Optional[int] = None


class LimitOrderStorage(BaseStorage[LimitOrderStorageModel]):
    key = "limit_order"
    model_class = LimitOrderStorageModel

