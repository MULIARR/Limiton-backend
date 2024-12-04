from pydantic import BaseModel

from constants import CryptoLogo


class TonMetadataModel(BaseModel):
    symbol: str = "TON"
    name: str = "Toncoin"
    image: str = CryptoLogo.TON
    decimals: int = 9
