from pydantic import BaseModel
from typing import Optional


class OrderCreate(BaseModel):
    user_id: int

    send_amount: float
    send_token_address: str
    send_token_symbol: str
    send_token_decimals: int
    send_token_image: str

    receive_amount: float
    receive_token_address: str
    receive_token_symbol: str
    receive_token_decimals: int
    receive_token_image: str

    minimum_to_receive_amount: float
    slippage: int

    profit_in_usd: Optional[float]
