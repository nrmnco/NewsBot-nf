import re

from aiogram.filters import BaseFilter
from aiogram.types import Message


class NameFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Two words
        # Cyrillic only
        # No numbers
        # No special symbols

        input_string = message.text

        print(len(input_string.split()) == 2)
        print(bool(re.match(r'^[а-яәіңғүұқөһА-ЯӘІҢҒҮҰҚӨҺёЁ\s]+$', input_string)))
        print(not any(char.isdigit() for char in input_string))

        return (
                len(input_string.split()) == 2 and
                bool(re.match(r'^[а-яәіңғүұқөһА-ЯӘІҢҒҮҰҚӨҺёЁ\s]+$', input_string)) and
                not any(char.isdigit() for char in input_string)
        )


class RoomFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        # Integer [1, 999]

        input_string = message.text

        return (
            input_string.isdigit()
            and 1 <= int(input_string) <= 999
        )
