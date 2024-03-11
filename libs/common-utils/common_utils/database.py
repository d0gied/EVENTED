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
    def get_events(name: str | None = None) -> list[Event]: ...

    @staticmethod
    @shared_task(name="update_event")
    def update_event(event: Event) -> None: ...

    @staticmethod
    @shared_task(name="delete_event")
    def delete_event(event_id: UUID) -> None: ...
