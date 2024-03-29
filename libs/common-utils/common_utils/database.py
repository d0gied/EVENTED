from datetime import datetime
from typing import Literal
from uuid import UUID

from celery import shared_task
from common_utils.models.event import Event, EventDict


class IDatabase:

    @staticmethod
    @shared_task(name="add_event", queue="database")
    def add_event(event: Event) -> None: ...

    @staticmethod
    @shared_task(name="get_event", queue="database")
    def get_event(event_id: int) -> Event | None: ...

    @staticmethod
    @shared_task(name="get_events", queue="database")
    def get_events() -> list[Event]: ...

    @staticmethod
    @shared_task(name="find_events", queue="database")
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
    ) -> list[tuple[Event, int]]: ...

    @staticmethod
    @shared_task(name="update_event", queue="database")
    def update_event(event: Event) -> None: ...

    @staticmethod
    @shared_task(name="delete_event", queue="database")
    def delete_event(event_id: int) -> None: ...

    @staticmethod
    @shared_task(name="subscribe", queue="database")
    def subscribe(user_id: int, tag: str | None = None) -> None: ...

    @staticmethod
    @shared_task(name="unsubscribe", queue="database")
    def unsubscribe(user_id: int, tag: str | None = None) -> None: ...

    @staticmethod
    @shared_task(name="subscribers", queue="database")
    def subscribers(tag: str) -> None: ...

    @staticmethod
    @shared_task(name="new_events", queue="database")
    def new_events() -> list[EventDict]: ...
