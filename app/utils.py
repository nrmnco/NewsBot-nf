import asyncio
import importlib
import pkgutil
import traceback

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from pydantic import BaseModel, root_validator
from bson import ObjectId
from typing import Any, Callable, Optional, Tuple
from zoneinfo import ZoneInfo

from datetime import datetime, date

import orjson


def import_routers(package_name):
    package = importlib.import_module(package_name)
    prefix = package.__name__ + "."

    for _, module_name, _ in pkgutil.iter_modules(package.__path__, prefix):
        # if not module_name.startswith(prefix + "router_"):
        #     continue

        try:
            importlib.import_module(module_name)
        except Exception as e:
            print(f"Failed to import {module_name}, error: {e}")
            traceback.print_exc()


def orjson_dumps(v: Any, *, default: Optional[Callable[[Any], Any]]) -> str:
    return orjson.dumps(v, default=default).decode()


# def convert_to_gmt(dt: datetime | date):
#     print("WE ARE CONVERTing YEAH")
#     if isinstance(dt, datetime):
#         if not dt.tzinfo:
#             dt = dt.replace(tzinfo=ZoneInfo("UTC"))
#         return dt.strftime("%Y-%m-%dT%H:%M:%S%z")
#     elif isinstance(dt, date):
#         return dt.strftime("%Y-%m-%d")
#     else:
#         raise ValueError("Unsupported type. Only datetime.datetime and datetime.date objects are supported.")
#

# def convert_to_gmt(dt: datetime | date):
#     if isinstance(dt, date):
#         # Convert date to datetime by assuming midnight time (00:00:00)
#         dt = datetime.combine(dt, datetime.min.time())
#         dt = dt.replace(tzinfo=ZoneInfo("UTC"))
#     else:
#         raise ValueError("Unsupported type. Only datetime.datetime and datetime.date objects are supported.")
#
#     if not dt.tzinfo:
#         dt = dt.replace(tzinfo=ZoneInfo("UTC"))
#
#     dt = dt.replace(tzinfo=ZoneInfo("UTC"))

    return dt.strftime("%Y-%m-%dT%H:%M:%S%z")

class AppModel(BaseModel):
    class Config:
        print('config')
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps
        # json_encoders = {datetime: convert_to_gmt, date: convert_to_gmt, ObjectId: str}

    @root_validator()
    def set_null_microseconds(cls, data: dict[str, Any]) -> dict[str, Any]:
        datetime_fields = {
            k: v.replace(microsecond=0)
            for k, v in data.items()
            if isinstance(k, datetime)
        }

        return {**data, **datetime_fields}


async def clear_history(state: FSMContext):
    await state.update_data(state_history=[])


async def append_history(handler: Callable, state: FSMContext):
    state_dict = {
        'state': await state.get_state(),
        'handler': handler
    }

    data = await state.get_data()
    history = data['state_history']
    history.append(state_dict)
    await state.update_data(state_history=history)
    print(history)


async def pop_history(state: FSMContext) -> Tuple[State, Callable]:
    data = await state.get_data()
    history = data['state_history']
    prev_state = history.pop()

    await state.update_data(state_history=history)

    return prev_state['state'], prev_state['handler']

