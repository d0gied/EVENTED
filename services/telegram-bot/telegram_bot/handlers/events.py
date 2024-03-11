from datetime import datetime

from aiogram import Router, types
from aiogram.filters import Command
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict

router = Router()


def date_fmt(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


@router.message(Command("events"))
async def get_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"later_than": datetime.now()}
    ).get()  # type: ignore

    if not events:
        await message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(Command("hackathon"))
async def get_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"later_than": datetime.now(), "type": "hackathon"}
    ).get()  # type: ignore

    if not events:
        await message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(Command("meetups"))
async def get_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"later_than": datetime.now(), "type": "meetup"}
    ).get()  # type: ignore

    if not events:
        await message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(Command("ai"))
async def get_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"later_than": datetime.now(), "tag": "ai"}
    ).get()  # type: ignore

    if not events:
        await message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


async def send_events(message: types.Message, events: list[Event]):
    for event in events:
        url = "https://codenrock.com/contests/" + str(event.id)
        msg = f"<a href='{url}'>{event.name}</a>\n"
        msg += f"Тип: {event.type}\n"
        if event.tags:
            tags = list(map(lambda tag: f"#{tag.name_ru}", event.tags))
            msg += f"Теги: {', '.join(tags)}\n"
        if event.prize:
            msg += f"Призы: {event.prize}\n"
        if event.start_date:
            msg += f"Начало: {date_fmt(event.start_date)}\n"
        if event.end_date:
            msg += f"Конец: {date_fmt(event.end_date)}\n"
        if event.start_registration and event.end_registration:
            msg += f"Регистрация: {date_fmt(event.start_registration)} - {date_fmt(event.end_registration)}\n"
        elif event.start_registration:
            msg += f"Регистрация с: {date_fmt(event.start_registration)}\n"
        elif event.end_registration:
            msg += f"Регистрация до: {date_fmt(event.end_registration)}\n"

        image = event.url
        if image:
            await message.answer_photo(image, caption=msg, parse_mode="HTML")
        else:
            await message.answer(msg, parse_mode="HTML")
