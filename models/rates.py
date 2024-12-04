from typing import Union

from pydantic import BaseModel


class SwapRates(BaseModel):
    send_amount_rate_in_usd: Union[int, float]
    receive_amount_rate_in_usd: Union[int, float]
    profit_percent: Union[int, float]  # 10
    profit_in_usd: Union[int, float]
    profit: str  # like +10%
