import redis.asyncio as aioredis
from dotenv import load_dotenv
import os

load_dotenv()

redis_client = aioredis.Redis(host=os.environ['HOST_NAME'], port=int(os.environ['PORT']))  # noqa
