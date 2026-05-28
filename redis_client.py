import redis.asyncio as aioredis
from dotenv import load_dotenv
import os

load_dotenv()

# redis_client = aioredis.Redis(host=os.environ['HOST_NAME'], port=int(os.environ['PORT']))  # noqa

# та же ошибка что и с mongodb
# redis_client создавался глобально при импорте модуля и привязывался к первому event loop.
# При следующем тесте с новым loop - падал.


def get_redis_client():
    redis_client = aioredis.Redis(host=os.environ['HOST_NAME'], port=int(os.environ['PORT']))  # noqa
    return redis_client
