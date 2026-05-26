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


async def get_activity(user_id):
    pipeline = [
        # это первый этап - фильтрация по user_id
        {"$match": {"user_id": user_id}},
        {
            # это второй этап - группировка
            '$group': {
                '_id': '$event_type',  # по полю event_type
                'operations_count': {  # это кастомное название для агрегации
                    '$sum': 1  # это операция при агрегации - сумма
                }
            }
        }
    ]

    query = await events_log.aggregate(pipeline)

    return await query.to_list()
