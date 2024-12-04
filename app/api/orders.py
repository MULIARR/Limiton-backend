from fastapi import APIRouter, HTTPException

from clients import ton
from database.db import db
from models.order import LimitOrderModel

orders_router = APIRouter(
    prefix="/orders"
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
async def get_order(order: LimitOrderModel):
    """
    Endpoint to create new limit order and launch it

    :param order:
    :return:
    """

    order_data = order.model_dump(
        include={
            'user_id',
            'type',
            'send_amount',
            'send_token_address',
            'receive_amount',
            'receive_token_address',
            'minimum_to_receive_amount',
            'slippage'
        }
    )

    # db entry
    order = await db.limit_orders.add_order(**order_data)

    # create limit order
    limit_order = await ton.limit_orders.create_limit_order_model(order)

    # launch limit order
    await ton.limit_orders.launch_limit_order(limit_order)

    return True


@orders_router.delete("/{order_id}", response_model=str)
async def delete_order(order_id: str):
    """
    Endpoint to delete/stop limit order

    :param order_id:
    :return:
    """

    # delete order from db
    order = await db.limit_orders.delete_order(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # stop task
    is_cancelled = ton.order_tasks.cancel_task(order_id)

    if is_cancelled:
        return f"Order with id {order_id} has been deleted"
    else:
        raise HTTPException(status_code=404, detail="Order not cancelled")
