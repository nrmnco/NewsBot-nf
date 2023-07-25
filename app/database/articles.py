from __future__ import annotations

from pymongo.database import Database, Collection
from pydantic import BaseModel, Field
from pydantic.types import Optional
from bson.objectid import ObjectId
from typing import List
import uuid

from datetime import datetime, timedelta, date

from app.utils import AppModel
from app.database import database


class Article(AppModel):
    title: str
    content: str
    url: str
    topics: list
    date: str = str(date.today())

class ArticleCollection:
    col: Collection = database['articles']

    @classmethod
    def create_article(cls, u: Article):

        result = cls.col.insert_one(u.dict())

        if result.acknowledged:
            return result.inserted_id
        else:
            return False

    @classmethod
    def get_articles_by_date(cls, date: date):

        result = cls.col.find({'date': date})

        return result


    @classmethod
    def get_article_by_url(cls, url: str):

        result = cls.col.find_one({'url': url})

        if result is None:
            return None
        return Article(**result)


    @classmethod
    def get_all_todays_articles(cls, date: str = str(date.today())):
        result = cls.col.find({'date': date})

        return [Article(**data) for data in result]


    @classmethod
    def get_users_by_room_number(cls, id: str):

        if not isinstance(id, ObjectId):
            id = ObjectId(id)

        result = cls.col.find(
            {'_id': id}
        )

        return [Article(**data) for data in result]
