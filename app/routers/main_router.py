from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import types


from app.database.user import User, UserCollection
from app.database.articles import Article, ArticleCollection
from app.states import MainState, FakeNewsState
from app.keyboards import main_menu
from app.utils import *
from app.adapters import bbc_parser, ai


import time
import asyncio

router = Router()

callbacks = {
    'reportazhi': 'Специальные репортажи и интервью',
    'politika': 'Политика и международные отношения',
    'ekonomika': 'Экономика и финансы',
    'obschestvo': 'Общественные проблемы и социальная сфера',
    'nauka': 'Наука и технологии',
    'zdravoohranenie': 'Здравоохранение и медицина',
    'kultura': 'Культура искусство и развлечения',
    'sport': 'Спорт и спортивные события',
    'ekologiya': 'Экология и природные ресурсы',
    'obrazovanie': 'Образование и научные исследования',
    'kriminal': 'Криминальная хроника и правоохранительные органы',
    'turizm': 'Туризм и путешествия',
    'religiya': 'Религия и вероисповедания',
    'transport': 'Транспорт и инфраструктура',
    'voennye': 'Военные события и безопасность',
    'migraciya': 'Миграция и беженцы',
    'innovacii': 'Инновации и стартапы',
    'pomoshch': 'Гуманитарная помощь и благотворительность',
    'sobytiya_mir': 'События в мире и геополитика',
    'sobytiya_strana': 'События в стране и региональные новости',
}

topics = set()


@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    await clear_history(state)

    user = UserCollection.get_user_by_tg_id(message.from_user.id)

    if user == None:
        await state.set_state(MainState.new_user)
        await message.answer('Драсте, выберите темы', reply_markup=main_menu.get_new_user())
    else:
        await state.set_state(MainState.stop)
        await message.answer("Аккаунт существует, нажмите на кнопку чтобы начать рассылку новостей", reply_markup=main_menu.start_news())


@router.message(Command('check_news'))
async def check_news_command(message: types.Message, state: FSMContext):
    await message.answer('Напишите новость, которую хотите проверить')
    await state.set_state(FakeNewsState.check)


@router.message(F.text == 'Остановить бота')
async def stop_state(message: types.Message, state: FSMContext):
    await state.update_data(stop=1)
    task.cancel()
    try:
        # Wait for the task to be cancelled
        await task
    except asyncio.CancelledError:
        pass
    await message.answer('Поток новостей остановлен', reply_markup=main_menu.start_news())
    await state.set_state(MainState.start)
    await clear_history(state)


@router.message(MainState.stop)
async def main_state(message: types.Message, state: FSMContext):
    await message.answer('Поток новостей запущен\n', reply_markup=main_menu.stop_news())
    print(await state.get_state())
    articles = ArticleCollection.get_all_todays_articles()

    user = UserCollection.get_user_by_tg_id(message.from_user.id)

    # main functionality aka lyutyi govnokod
    for a in articles:
        if any(topic in user.topics for topic in a.topics) and a.url not in user.received_articles:
            resp = "<b>" + a.title + "</b>" + '\n\n' + a.content + '\n\n' + a.url
            await message.answer(resp, parse_mode='HTML')
            interests = user.received_articles
            interests.append(a.url)
            UserCollection.update_user_articles(interests, message.from_user.id)
            time.sleep(5)
    global task
    task = asyncio.create_task(main_func(user, message, state))


@router.message(F.text == 'Запустить бота')
async def start_state(message: types.Message, state: FSMContext):
    await state.update_data(stop=0)
    await state.set_state(MainState.stop)
    await message.answer('Поток новостей запущен\n', reply_markup=main_menu.stop_news())


@router.callback_query(MainState.new_user)
async def handle_callback_query(callback: CallbackQuery, state: FSMContext):
    if callback.data in callbacks:
        await handle_queries(callback)
    else:
        await callback.message.delete()

        new_user = User(
            tg_id=callback.from_user.id,
            topics=list(topics)
        )

        UserCollection.create_user(new_user)
        await state.set_state(MainState.stop)
        await callback.message.answer('Ваши интересы сохранены')
        await callback.message.answer('Нажмите на кнопку чтобы запустить рассылку новостей', reply_markup=main_menu.start_news())


async def handle_queries(callback: CallbackQuery):
    # Generate a random value and send it as a message
    topics.add(callbacks[callback.data])
    await callback.answer()


async def main_func(user, message, state: FSMContext):
    while True:
        url = "https://www.bbc.com/news/world"

        links = bbc_parser.get_all_todays_urls(url)
        print(links)
        links = set(links)
        for link in links:
            if ArticleCollection.get_article_by_url(link) is None:

                print(link)

                try:
                    title = bbc_parser.get_title(link)
                    content = bbc_parser.get_article_text(link)
                    url = link
                    if content == '':
                        print('video')
                        continue

                except Exception as e:
                    print(e)
                    print('error')
                    continue

                ai.new_article()
                brief_content = ai.paraphrase(content)
                topics = ai.get_themes(content)

                article = {
                    'title': title,
                    'content': brief_content,
                    'url': url,
                    'topics': topics
                }
                print(article)

                if any(topic in user.topics for topic in topics) and article['url'] not in user.received_articles:
                    resp = "<b>" + article['title'] + "</b>" + '\n\n' + article['content'] + '\n\n' + article['url']
                    await message.answer(resp, parse_mode='HTML')
                    print('message sended')
                    interests = user.received_articles
                    interests.append(article['url'])
                    UserCollection.update_user_articles(interests, message.from_user.id)

                    ArticleCollection.create_article(Article(**article))
                    print('saved')
                else:
                    print(content)

                if await state.get_state() != 'MainState:stop':
                    print(await state.get_state())
                    print('inner stop')
                    break

                print('ждем 40 секунд')
                await asyncio.sleep(40)

        if await state.get_state() != 'MainState:stop':
            print(await state.get_state())
            print('outer stop')
            break
        print('ждем час')
        await asyncio.sleep(3600)