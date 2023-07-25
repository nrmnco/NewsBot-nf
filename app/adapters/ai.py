import openai

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

from app.config import config

import os

# from prompts import theme_prompt, paraphrase_prompt



theme_prompt = """Which topics listed below does this article relate to?
-Политика и международные отношения
-Экономика и финансы
-Общественные проблемы и социальная сфера
-Наука и технологии
-Здравоохранение и медицина
-Культура искусство и развлечения
-Спорт и спортивные события
-Экология и природные ресурсы
-Образование и научные исследования
-Криминальная хроника и правоохранительные органы
-Туризм и путешествия
-Религия и вероисповедания
-Транспорт и инфраструктура
-Военные события и безопасность
-Миграция и беженцы
-Инновации и стартапы
-Гуманитарная помощь и благотворительность
-События в мире и геополитика
-События в стране и региональные новости
-Специальные репортажи и интервью.
If it is related, then in response write only a list of topics that are related to the article. Do not write anything other than topics. For example, if the article concerns the topics 'Политика и международные отношения' and 'Экономика и финансы' then simply write them separated by commas without spaces after the comma in russian language, as in this example 'Политика и международные отношения,Экономика и финансы'"""


paraphrase_prompt = """Write a short description of this article, including all the most important things in the description. The description should not exceed 100 words. Do not write anything other than the description itself"""
api_key = config.OPENAI_API_KEY.get_secret_value()
openai.api_key = api_key
# Ты человек ведущий новостной телеграм канал, который кратко описывает новости статей из разных сайтов

def new_article():
    global messages
    global system_msg
    messages = []
    system_msg = "You are a person leading a telegram news channel that briefly describes the news of articles from different sites"
    messages.append({'role': 'system', 'content': system_msg})


def paraphrase(text):
    prompt = text + "\n" + paraphrase_prompt
    messages.append({'role': 'user', 'content': text})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    reply = response['choices'][0]['message']['content']
    return reply


# получает ответ в виде строки с темами, нужно их отделить и поместить в список themes
def get_themes(text):
    prompt = text + "\n" + theme_prompt
    messages.append({'role': 'user', 'content': prompt})
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages
    )
    reply = response['choices'][0]['message']['content']
    reply = reply.split(',')

    for i, value in enumerate(reply):
        if value[0] == ' ':
            reply[i] = value[1:]

    return reply


os.environ['OPENAI_API_KEY'] = api_key
os.environ['SERPAPI_API_KEY'] = config.SERP_API_KEY.get_secret_value()
llm = OpenAI(temperature=0)

tools = load_tools(["serpapi"], llm=llm)

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

def fakenews(news: str):
    return agent.run("is this statement true? '" + news + "'")

