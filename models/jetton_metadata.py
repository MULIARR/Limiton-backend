from pydantic import BaseModel


class JettonMetadataModel(BaseModel):
    symbol: str
    name: str
    image: str
    decimals: int
