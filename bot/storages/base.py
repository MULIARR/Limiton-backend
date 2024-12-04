import logging
from abc import ABC
from typing import TypeVar, Generic, Type, Dict, Any
from aiogram.fsm.context import FSMContext
from pydantic import BaseModel, ValidationError

T = TypeVar('T', bound=BaseModel)


logger = logging.getLogger(__name__)


class BaseStorage(ABC, Generic[T]):
    key: str
    model_class: Type[T]

    @classmethod
    async def get(cls, state: FSMContext) -> T:
        data = await state.get_data()

        if cls.key not in data:
            model_instance = cls.model_class()
            await state.update_data(**{cls.key: model_instance.dict()})
        else:
            try:
                model_instance = cls.model_class(**data[cls.key])
            except ValidationError as e:
                logger.error(f"{cls.key} model validation error: {e}")
                model_instance = cls.model_class()

        return model_instance

    @classmethod
    async def update(cls, state: FSMContext, **kwargs) -> T:
        model_instance = await cls.get(state)
        try:
            updated_model = model_instance.model_copy(update=kwargs)
        except ValidationError as e:
            logger.info(f"{cls.key} model validation error: {e}")
            return
        await state.update_data(**{cls.key: updated_model.model_dump()})
        return updated_model

    @classmethod
    async def clear(cls, state: FSMContext):
        data = await state.get_data()
        if cls.key in data:
            del data[cls.key]
            await state.set_data(data)
