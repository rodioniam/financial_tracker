from pymongo import AsyncMongoClient

from dotenv import load_dotenv
import os

load_dotenv()

mongo_db = AsyncMongoClient(os.environ['MONGO_URL'])  # подключение к серверу
db = mongo_db['fin_tracker']  # создание базы данных
# создание коллекции, аналог таблицы. Именно это будет являться объектом для взаимодействия с базой - вставка, поиск, агрегация
events_log = db['events_log']


async def create_indexes():
    await events_log.create_index('user_id')
    await events_log.create_index('event_type')
