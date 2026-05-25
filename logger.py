from mongo_db import events_log
from datetime import datetime


async def log_event(event_type: str, user_id: int, details: dict):
    event = {
        'event_type': event_type,
        'timestamp': datetime.now(),
        'user_id': user_id,
        'details': details
    }

    await events_log.insert_one(event)
