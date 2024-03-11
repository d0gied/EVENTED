from typing import Literal
from uuid import UUID

from celery import shared_task
from common_utils.models.event import Event, EventDict


class IDatabase:

    @staticmethod
    @shared_task(name="add_event")
    def add_event(event: Event) -> None: ...

    @staticmethod
    @shared_task(name="get_event")
    def get_event(event_id: UUID) -> Event | None: ...

    @staticmethod
    @shared_task(name="get_events")
    def get_events() -> list[Event]: ...

    @staticmethod
    @shared_task(name="find_events")
    def find_events(
        name: str | None = None,
        tag: str | None = None,
        type: (
            Literal["projects", "ml", "remote", "hackathon", "meetup", "test"] | None
        ) = None,
        limit: int | None = None,
        threshold: int = 80,
    ) -> list[tuple[Event, int]]: ...

    @staticmethod
    @shared_task(name="update_event")
    def update_event(event: Event) -> None: ...

    @staticmethod
    @shared_task(name="delete_event")
    def delete_event(event_id: UUID) -> None: ...
