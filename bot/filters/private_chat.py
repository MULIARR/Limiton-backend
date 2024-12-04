from aiogram.filters import BaseFilter
from aiogram.types import Message


class IsPrivateChatFilter(BaseFilter):
    is_private: bool = True

    async def __call__(self, message: Message) -> bool:
        return (message.chat.type == 'private') == self.is_private
