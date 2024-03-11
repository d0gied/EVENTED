import json
import re
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
    @app.task(name="add_event")
    def add_event(event: EventDict) -> None:
        if repository.find_one({"id": event["id"]}) or repository.find_one(
            {"name": event["name"]}
        ):
            print("Event already exists")
            return
        repository.insert(event)

    @staticmethod
    @app.task(name="add_events")
    def add_events(events: list[EventDict]) -> None:
        for event in events:
            Database.add_event(event)

    @staticmethod
    @app.task(name="get_event")
    def get_event(event_id: UUID) -> EventDict | None:
        found = repository.find_one({"id": event_id})
        return Event(**found).model_dump() if found else None

    @staticmethod
    @app.task(name="get_events")
    def get_events() -> list[EventDict]:
        return [Event(**event).model_dump() for event in repository.find({})]

    @staticmethod
    @app.task(name="find_events")
    def find_events(
        name: str | None = None,
        tag: str | None = None,
        type: (
            Literal["projects", "ml", "remote", "hackathon", "meetup", "test"] | None
        ) = None,
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
            if score >= threshold:
                result.append((Event(**event).model_dump(), score))
        result = sorted(result, key=lambda x: -x[1])[:limit]
        if not result:
            return []
        return result

    @staticmethod
    def update_event(event: EventDict) -> None:
        _event = Event.model_validate(event)
        repository.update({"id": _event.id}, event)

    @staticmethod
    def delete_event(event_id: UUID) -> None:
        repository.delete({"id": event_id})
