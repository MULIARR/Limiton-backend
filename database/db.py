from config import config
from database.base import get_engine, get_session_local, Base

from database.repo import (
    UserRepository,
    OrderRepository,
    TonWalletRepository
)


class Database:
    def __init__(self, database_url: str):
        self.engine = get_engine(database_url)
        self.session_local = get_session_local(self.engine)

        self.user_repo = UserRepository(self.session_local)
        self.order_repo = OrderRepository(self.session_local)
        self.ton_wallet_repo = TonWalletRepository(self.session_local)

    async def async_init(self):
        async with self.engine.begin() as conn:
            ...
            # await conn.run_sync(Base.metadata.drop_all)
            # await conn.run_sync(Base.metadata.create_all)

    async def close(self):
        self.session_local.close_all()

    @property
    def users(self):
        return self.user_repo

    @property
    def limit_orders(self):
        return self.order_repo

    @property
    def ton_wallets(self):
        return self.ton_wallet_repo


db = Database(config.db.database_url)

# import all models (native import)
import database.schema
