from sqlalchemy import select, exists
from datetime import datetime

from database.schema import User


class UserRepository:
    def __init__(self, session_local):
        self.session_local = session_local

    async def add_user(
            self,
            user_id: int,
            language: str
    ) -> User:
        async with self.session_local() as session:
            user = User(
                user_id=user_id,
                language=language,
                join_date=datetime.utcnow()
            )

            session.add(user)
            await session.commit()

            return user

    async def user_exists(self, user_id: int) -> bool:
        async with self.session_local() as session:
            stmt = select(exists().where(User.user_id == user_id))
            result = await session.execute(stmt)
            return result.scalar() is True

    async def get_user(self, user_id: int) -> User:
        async with self.session_local() as session:
            result = await session.execute(
                select(User).filter_by(user_id=user_id)
            )
            return result.scalar()

    async def update_user_language(self, user_id: int, new_language: str) -> None:
        async with self.session_local() as session:
            user = await session.get(User, user_id)
            if user:
                user.language = new_language
                await session.commit()

    async def delete_user(self, user_id: int) -> None:
        async with self.session_local() as session:
            user = await session.get(User, user_id)
            if user:
                session.delete(user)
                await session.commit()
