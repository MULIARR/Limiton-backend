import asyncio
from typing import Coroutine, Any

from models.order import TaskModel, LimitOrderModel


class OrderTaskController:
    """
    task == launched order
    """
    def __init__(self) -> None:
        self.tasks: dict[str, TaskModel] = {}

    def create_task(
            self,
            order_id: str,
            coroutine: Coroutine[Any, Any, Any],
            order_model: LimitOrderModel
    ) -> asyncio.Task:
        if order_id in self.tasks:
            raise ValueError(f"Task with id '{order_id}' already exists.")

        task = asyncio.create_task(coroutine)

        self.tasks[order_id] = TaskModel(
            order_model=order_model,
            task=task
        )

        return task

    def cancel_task(self, order_id: str) -> asyncio.Task:
        if order_id not in self.tasks:
            return False

        task = self.tasks.pop(order_id).task
        task.cancel()
        return task

    def get_task(self, order_id: str) -> TaskModel:
        if order_id not in self.tasks:
            raise ValueError(f"Task with order id '{order_id}' does not exist.")
        return self.tasks[order_id]

    def get_active_user_orders(self, user_id: int):
        """
        Method to get all active (launched) user's orders

        :param user_id:
        :return:
        """
        return [
            task_model.order_model for _, task_model in self.tasks.items()
            if task_model.order_model.user_id == user_id
        ]

    def get_all_tasks(self) -> dict[str, TaskModel]:
        return self.tasks

    def restart_task(
            self,
            task_id: str,
    ) -> asyncio.Task:
        task = self.get_task(task_id)

        self.cancel_task(task_id)
        return self.create_task(task_id, task.task, task.order_model)

