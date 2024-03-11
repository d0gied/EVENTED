import json
import queue
import re
from datetime import datetime
from tracemalloc import start
from typing import Literal
from uuid import UUID

from celery import Celery
from common_utils.celery import get_app
from common_utils.config import CeleryConfig
from common_utils.database import Event, EventDict, IDatabase
from fuzzywuzzy import fuzz, process

from .mongo import MongoRepository

repository = MongoRepository("events")
app = get_app("database")


class Database(IDatabase):

    @staticmethod
    @app.task(name="add_event", queue="database")
    def add_event(event: EventDict) -> None:
        if repository.find_one({"id": event["id"]}) or repository.find_one(
            {"name": event["name"]}
        ):
            print("Event already exists")
            return
        repository.insert(event)

    @staticmethod
    @app.task(name="add_events", queue="database")
    def add_events(events: list[EventDict]) -> None:
        for event in events:
            Database.add_event(event)

    @staticmethod
    @app.task(name="get_event", queue="database")
    def get_event(event_id: UUID) -> EventDict | None:
        found = repository.find_one({"id": event_id})
        return Event(**found).model_dump() if found else None

    @staticmethod
    @app.task(name="get_events", queue="database")
    def get_events() -> list[EventDict]:
        return [Event(**event).model_dump() for event in repository.find({})]

    @staticmethod
    @app.task(name="find_events", queue="database")
    def find_events(
        name: str | None = None,
        tag: str | None = None,
        type: (
            Literal["projects", "ml", "remote", "hackathon", "meetup", "test"] | None
        ) = None,
        later_than: datetime | None = None,
        earlier_than: datetime | None = None,
        limit: int | None = None,
        threshold: int = 80,
    ) -> list[tuple[Event, int]]:
        events = repository.find({})
        result = list()
        for event in events:
            score = 100
            if name:
                score = min(
                    score, fuzz.token_set_ratio(name.lower(), event["name"].lower())
                )
            if tag:
                _score = 0
                for _tag in event["tags"]:
                    _score = max(
                        _score,
                        fuzz.token_set_ratio(tag.lower(), _tag["name_ru"].lower()),
                    )
                    _score = max(
                        _score,
                        fuzz.token_set_ratio(tag.lower(), _tag["name_en"].lower()),
                    )
                score = min(score, _score)
            if type:
                score = min(
                    score, fuzz.token_set_ratio(type.lower(), event["type"].lower())
                )
            date = event["end_date"]
            if date is None:
                date = event["start_date"]
            if date is None:
                date = event["end_registration"]
            if date is None:
                date = event["start_registration"]
            if later_than:
                if date is None or date < later_than:
                    score = 0

            if earlier_than:
                if date is None or date > earlier_than:
                    score = 0

            if score >= threshold:
                result.append((Event(**event).model_dump(), score))
        result = sorted(result, key=lambda x: -x[1])[:limit]
        if not result:
            return []
        return result

    @staticmethod
    @app.task(name="update_event", queue="database")
    def update_event(event: EventDict) -> None:
        _event = Event.model_validate(event)
        repository.update({"id": _event.id}, event)

    @staticmethod
    @app.task(name="delete_event", queue="database")
    def delete_event(event_id: int) -> None:
        repository.delete({"id": event_id})
