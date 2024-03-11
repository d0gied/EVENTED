from uuid import UUID

from celery import Celery
from celery.result import AsyncResult
from common_utils.celery import get_app
from common_utils.config import CeleryConfig
from common_utils.database import IDatabase
from common_utils.models.event import Event
from fastapi import APIRouter

router = APIRouter(tags=["event"], prefix="/event")
app = get_app("api")


@router.get("/")
async def get_events(name: str | None = None):
    task: AsyncResult = IDatabase.get_events.apply_async(args=[name])
    return str(task.get())


@router.post("/add/")
async def add_event(event: Event):
    task: AsyncResult = IDatabase.add_event.apply_async(args=[event.model_dump()])
    return str(task.get())


@router.get("/{event_id}")
async def get_event(event_id: UUID):
    task: AsyncResult = IDatabase.get_event.apply_async(args=[event_id])
    return str(task.get())


# @router.post("add/")
# def add_event():
#     return {"event": "event"}
