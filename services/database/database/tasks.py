import json
from uuid import UUID

from celery import Celery
from common_utils.celery import get_app
from common_utils.config import CeleryConfig
from common_utils.database import Event, EventDict, IDatabase

from .mongo import MongoRepository

repository = MongoRepository("events")
app = get_app("database")


class Database(IDatabase):

    @staticmethod
    @app.task(name="add_event")
    def add_event(event: EventDict) -> None:
        repository.insert(event)

    @staticmethod
    @app.task(name="get_event")
    def get_event(event_id: UUID) -> EventDict | None:
        found = repository.find_one({"id": event_id})
        return Event(**found).model_dump() if found else None

    @staticmethod
    @app.task(name="get_events")
    def get_events(name: str | None = None) -> list[EventDict]:
        if name:
            return [
                Event(**event).model_dump() for event in repository.find({"name": name})
            ]
        else:
            return [Event(**event).model_dump() for event in repository.find({})]

    @staticmethod
    def update_event(event: EventDict) -> None:
        _event = Event.model_validate(event)
        repository.update({"id": _event.id}, event)

    @staticmethod
    def delete_event(event_id: UUID) -> None:
        repository.delete({"id": event_id})
