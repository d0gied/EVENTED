from celery import Celery

from .config import CeleryConfig


def get_app(name: str) -> Celery:
    app = Celery(
        name,
        broker=CeleryConfig().celery_broker,
        backend=CeleryConfig().celery_backend,
    )
    app.conf.update(
        timezone="Europe/Moscow",
        enable_utc=True,
    )
    return app
