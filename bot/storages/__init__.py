"""
Package "storage" is a wrapper over aiogram FSMContext,
allowing storage and updating of data for each user
in the form of Pydantic models.

Models are managed by generic class BaseStorage.
"""


from .limit_order import LimitOrderStorage


class Storages:
    def __init__(self):
        self.limit_order = LimitOrderStorage()


storages = Storages()

__all__ = ["storages"]
