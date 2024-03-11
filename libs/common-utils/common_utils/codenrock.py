from celery import shared_task
from common_utils.models.event import Event, EventDict


class ICodenrock:

    @staticmethod
    @shared_task(name="codenrock.get_events", queue="codenrock")
    def get_events() -> list[EventDict]: ...

    @staticmethod
    @shared_task(name="codenrock.parse", queue="codenrock")
    def parse(): ...
