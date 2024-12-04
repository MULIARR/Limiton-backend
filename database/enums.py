from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
