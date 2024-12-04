from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional

from database.base import Base
from datetime import datetime


class Order(Base):
    __tablename__ = 'orders'

    order_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), nullable=False)

    send_amount: Mapped[float] = mapped_column(nullable=False)
    send_token_address: Mapped[str] = mapped_column(nullable=False)
    send_token_symbol: Mapped[str] = mapped_column(nullable=False)
    send_token_image: Mapped[str] = mapped_column(nullable=False)

    receive_amount: Mapped[float] = mapped_column(nullable=False)
    receive_token_address: Mapped[str] = mapped_column(nullable=False)
    receive_token_symbol: Mapped[str] = mapped_column(nullable=False)
    receive_token_image: Mapped[str] = mapped_column(nullable=False)

    minimum_to_receive_amount: Mapped[float] = mapped_column(nullable=False)
    slippage: Mapped[int] = mapped_column(nullable=False)

    profit_in_usd: Mapped[float] = mapped_column(nullable=False)
    profit_in_ton: Mapped[float] = mapped_column(nullable=False)

    status: Mapped[str] = mapped_column(nullable=False)

    creation_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    completion_date: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def to_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.__table__.columns.keys()}
