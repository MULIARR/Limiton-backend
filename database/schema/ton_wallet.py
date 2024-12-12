from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, LargeBinary, String

from database.base import Base
from database.schema import User


class TonWallet(Base):
    __tablename__ = 'ton_wallets'

    wallet_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id'), unique=True, nullable=False)
    mnemonics: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    # name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped['User'] = relationship('User', back_populates='wallet')
