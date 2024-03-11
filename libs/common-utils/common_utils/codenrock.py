from celery import shared_task
from common_utils.models.event import Event, EventDict


class ICodenrock:
    @staticmethod
    @shared_task(name="codenrock.get_events")
    def get_events() -> list[EventDict]: ...

    @staticmethod
    @shared_task(name="codenrock.parse")
    def parse(): ...
