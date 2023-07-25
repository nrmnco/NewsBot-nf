import bson
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.database.user import User, UserCollection
from app.database.articles import Article, ArticleCollection
from app.states import MainState, FakeNewsState
from app.keyboards import main_menu
from app.adapters import bbc_parser, ai


router = Router()


@router.message(FakeNewsState.check)
async def check_news(message: types.Message, state: FSMContext):
    result = ai.fakenews(message.text)
    await message.answer(result, reply_markup=main_menu.start_news())
    await state.set_state(MainState.stop)