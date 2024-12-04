import asyncio
from typing import Union, Optional

from pydantic import BaseModel

from models.jetton_metadata import JettonMetadataModel
from models.ton_metadata import TonMetadataModel


class LimitOrderModel(BaseModel):
    order_id: Optional[str] = None
    user_id: int

    send_token_address: str
    send_amount: Union[int, float]
    send_token_metadata: Optional[Union[JettonMetadataModel, TonMetadataModel]] = None

    receive_token_address: str
    receive_amount: Union[int, float]
    receive_token_metadata: Optional[Union[JettonMetadataModel, TonMetadataModel]] = None

    slippage: Optional[int] = None
    minimum_to_receive_amount: Union[int, float] = 0


class TaskModel(BaseModel):
    order_model: LimitOrderModel
    task: asyncio.Task

    class Config:
        arbitrary_types_allowed = True

