from asyncio import CancelledError

from fastapi import APIRouter, HTTPException

from clients import ton
from clients.logger_config import app_logger
from database.db import db
from models.db.order import OrderCreate

orders_router = APIRouter(
    prefix="/order"
)


@orders_router.get("/all/{user_id}")
async def get_active_user_orders(user_id: int):
    """
    Endpoint to get all active (launched) user's orders

    :param user_id:
    :return:
    """

    for task in ton.order_tasks.tasks.values():
        print(task.order_model.order_id, task.task)

    orders = ton.order_tasks.get_active_user_orders(user_id)
    return orders

    # return [task_model.order_model for task_model in ton.order_tasks.get_all_tasks().values()]


@orders_router.get("/get/{order_id}")
async def get_order(order_id: str):
    return ton.order_tasks.get_task(order_id).order_model


@orders_router.post("/create")
async def get_order(order: OrderCreate):
    """
    Endpoint to create new limit order and launch it

    :param order:
    :return:
    """

    # db entry
    order = await db.limit_orders.add_order(**order.model_dump())

    # create limit order
    limit_order = await ton.limit_orders.create_limit_order_model(order)

    # launch limit order
    await ton.limit_orders.launch_limit_order(limit_order)

    return True


@orders_router.delete("/{order_id}", response_model=str)
async def delete_order(order_id: str):
    """
    Endpoint to delete/stop limit order
    """

    order = await db.limit_orders.delete_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or already cancelled")

    task = ton.order_tasks.cancel_task(order_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        await task
    except CancelledError:
        print(f"Task {order_id} was cancelled successfully")
    except Exception as e:
        print(f"Task {order_id} failed with exception: {e}")
        raise HTTPException(status_code=500, detail=f"Task failed: {e}")

    if task.done():
        if task.cancelled():
            return f"Order with id {order_id} has been deleted"
        elif task.exception():
            raise HTTPException(status_code=500, detail=f"Task failed with exception: {task.exception()}")
        else:
            return f"Order with id {order_id} completed successfully"
    else:
        raise HTTPException(status_code=500, detail="Task is still running")


