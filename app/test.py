import random
from bson import ObjectId
from datetime import datetime

from database.room import Room, RoomRating, RoomCollection
from database.user import User, UserCollection
from database.event import Event, EventsCollection

EventsCollection.create_event(
    Event(
        name='Поход в магазин',
        description='Групповой поход в магазин для покупки дихлофоса, покушать и попить (не выпить).',
        place='Магазин "Береке"',
        time=datetime(day=30, month=9, year=2023),
        host=ObjectId('649e340ec0c0ee14414f6a97')
    )
)

print(EventsCollection.get_upcoming_events())
