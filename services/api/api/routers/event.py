from typing import Literal
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


@router.get("/all")
async def get_events():
    task: AsyncResult = IDatabase.get_events.apply_async()
    return str(task.get())


@router.get("/find")
async def find_events(
    name: str | None = None,
    tag: str | None = None,
    type: (
        Literal["projects", "ml", "remote", "hackathon", "meetup", "test"] | None
    ) = None,
    limit: int | None = None,
    threshold: int = 80,
):
    task: AsyncResult = IDatabase.find_events.apply_async(
        kwargs={
            "name": name,
            "tag": tag,
            "type": type,
            "limit": limit,
            "threshold": threshold,
        }
    )  # type: ignore
    return str(task.get())


@router.post("/add/")
async def add_event(event: Event):
    task: AsyncResult = IDatabase.add_event.apply_async(args=[event.model_dump()])  # type: ignore
    return str(task.get())


@router.get("/{event_id}")
async def get_event(event_id: int):
    task: AsyncResult = IDatabase.get_event.apply_async(args=[event_id])  # type: ignore
    return str(task.get())


# @router.post("add/")
# def add_event():
#     return {"event": "event"}
