import string
from datetime import datetime
import random

from sqlalchemy import select

from database.enums import OrderStatus
from database.schema.order import Order


class OrderRepository:
    def __init__(self, session_local):
        self.session_local = session_local

    async def add_order(
            self,
            user_id: int,
            send_amount: float,
            send_token_address: str,
            receive_amount: float,
            receive_token_address: str,
            minimum_to_receive_amount: float,
            slippage: int,
            status: str = OrderStatus.ACTIVE.value,
            completion_date: datetime = None
    ) -> Order:
        async with self.session_local() as session:
            order_id = await self.generate_unique_order_id()

            order = Order(
                order_id=order_id,
                user_id=user_id,
                send_amount=send_amount,
                send_token_address=send_token_address,
                receive_amount=receive_amount,
                receive_token_address=receive_token_address,
                minimum_to_receive_amount=minimum_to_receive_amount,
                slippage=slippage,
                status=status,
                completion_date=completion_date
            )
            session.add(order)
            await session.commit()
            return order

    async def get_order(self, order_id: str) -> Order:
        async with self.session_local() as session:
            return session.query(Order).filter(Order.order_id == order_id).first()

    async def get_orders(self, user_id: int) -> list[Order]:
        """
        (Non-actual) Method to get all user's active orders

        :param user_id:
        :return:
        """
        async with self.session_local() as session:
            result = await session.execute(
                select(Order).filter(
                    (Order.user_id == user_id) & (Order.status == OrderStatus.ACTIVE.value)
                )
            )
            return result.scalars().all()

    async def get_active_orders(self) -> list[Order]:
        async with self.session_local() as session:
            result = await session.execute(select(Order).filter(Order.status == OrderStatus.ACTIVE.value))
            return result.scalars().all()

    async def update_order_status(self, order_id: str, new_status: str) -> None:
        async with self.session_local() as session:
            result = await session.execute(select(Order).where(Order.order_id == order_id))
            order = result.scalar_one_or_none()
            if order:
                order.status = new_status
                await session.commit()

    async def delete_order(self, order_id: str) -> bool:
        async with self.session_local() as session:
            result = await session.execute(select(Order).filter(Order.order_id == order_id))
            order = result.scalars().first()
            if order:
                await session.delete(order)
                await session.commit()
                return True

            return False

    async def generate_unique_order_id(self) -> str:
        while True:
            order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not await self.is_order_id_exists(order_id):
                break
        return order_id

    async def is_order_id_exists(self, order_id: str) -> bool:
        async with self.session_local() as session:
            result = await session.execute(
                select(Order).filter_by(order_id=order_id)
            )
            return result.scalar() is not None
