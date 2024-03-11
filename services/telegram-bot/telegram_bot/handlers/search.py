from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.filters import Command
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict

from .events import send_events

router = Router()


def date_fmt(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


@router.message(F.text[0] == "#")
async def search_events(message: types.Message):  # type: ignore
    request = message.text

    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"tag": request[1:], "threshold": 50, "limit": 5}  # type: ignore
    ).get()  # type: ignore

    events = [Event.model_validate(event) for event, score in events[:5]]  # type: ignore
    await send_events(message, events)  # type: ignore


@router.message(F.text[0] != "/")
async def search_events(message: types.Message):
    request = message.text

    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"name": request, "threshold": 50, "limit": 5}
    ).get()  # type: ignore
    events += IDatabase.find_events.apply_async(
        kwargs={"tag": request, "threshold": 50, "limit": 5}
    ).get()  # type: ignore
    events += IDatabase.find_events.apply_async(
        kwargs={"type": request, "threshold": 50, "limit": 5}
    ).get()  # type: ignore

    if not events:
        await message.answer("Мероприятий не найдено")
        return

    events_dict = {}
    for event, score in events:
        if event["id"] not in events_dict:
            events_dict[event["id"]] = (event, score)
        else:
            events_dict[event["id"]] = (
                event,
                events_dict[event["id"]][1] + score,
            )

    events = list(events_dict.values())
    events.sort(key=lambda x: x[1], reverse=True)
    events = [Event.model_validate(event) for event, score in events[:5]]  # type: ignore
    await send_events(message, events)  # type: ignore
