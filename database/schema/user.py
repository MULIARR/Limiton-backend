from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime

from database.base import Base


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    language: Mapped[str] = mapped_column(ENUM('en', 'ru', 'ua', name='language_code'), nullable=False)
    join_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    wallet: Mapped['TonWallet'] = relationship('TonWallet', back_populates='user', uselist=False)  # 1 to 1
