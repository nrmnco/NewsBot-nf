import aiogram.types
from aiogram import types
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup

BUTTON_NAMES = [
    ['reportazhi', 'Специальные репортажи и интервью'],
    ['politika', 'Политика и международные отношения'],
    ['ekonomika', 'Экономика и финансы'],
    ['obschestvo', 'Общественные проблемы и социальная сфера'],
    ['nauka', 'Наука и технологии'],
    ['zdravoohranenie', 'Здравоохранение и медицина'],
    ['kultura', 'Культура, искусство и развлечения'],
    ['sport', 'Спорт и спортивные события'],
    ['ekologiya', 'Экология и природные ресурсы'],
    ['obrazovanie', 'Образование и научные исследования'],
    ['kriminal', 'Криминальная хроника и правоохранительные органы'],
    ['turizm', 'Туризм и путешествия'],
    ['religiya', 'Религия и вероисповедания'],
    ['transport', 'Транспорт и инфраструктура'],
    ['voennye', 'Военные события и безопасность'],
    ['migraciya', 'Миграция и беженцы'],
    ['innovacii', 'Инновации и стартапы'],
    ['pomoshch', 'Гуманитарная помощь и благотворительность'],
    ['sobytiya_mir', 'События в мире и геополитика'],
    ['sobytiya_strana', 'События в стране и региональные новости'],
    ['ready', 'Готово']
]


def stop_news():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Остановить бота')]
        ]
    )


def start_news():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Запустить бота')]
        ]
    )


def get_new_user():
    builder = InlineKeyboardBuilder()

    for button in BUTTON_NAMES:
        builder.add(types.InlineKeyboardButton(text=button[1], callback_data=button[0]))

    builder.adjust(2)

    return builder.as_markup()
