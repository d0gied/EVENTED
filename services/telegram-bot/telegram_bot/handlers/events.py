from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.filters import Command
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict

router = Router()


def date_fmt(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


events_keyboard = types.ReplyKeyboardMarkup(
    keyboard=[
        [types.KeyboardButton(text="Всё")],
        [
            types.KeyboardButton(text="Все хакатоны"),
            types.KeyboardButton(text="Все митапы"),
            types.KeyboardButton(text="Все нейронки"),
        ],
        [
            types.KeyboardButton(text="Всё за неделю"),
            types.KeyboardButton(text="Всё за месяц"),
            types.KeyboardButton(text="Всё за год"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите категорию",
)


@router.message(F.text == "Всё")
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


@router.message(F.text == "Все хакаторы")
@router.message(Command("hackathons"))
async def get_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={"later_than": datetime.now(), "type": "hackathon"}
    ).get()  # type: ignore

    if not events:
        await message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(F.text == "Все митапы")
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


@router.message(F.text == "Все нейронки")
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


@router.message(F.text == "Всё за неделю")
@router.message(Command("week"))
async def get_recent_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={
            "later_than": datetime.now() - timedelta(days=7),
            "earlier_than": datetime.now(),
        }
    ).get()  # type: ignore

    if not events:
        message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(F.text == "Всё за месяц")
@router.message(Command("month"))
async def get_recent_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={
            "later_than": datetime.now() - timedelta(days=30),
            "earlier_than": datetime.now(),
        }
    ).get()  # type: ignore

    if not events:
        message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


@router.message(F.text == "Всё за год")
@router.message(Command("year"))
async def get_recent_events(message: types.Message):
    events: list[tuple[EventDict, int]] = IDatabase.find_events.apply_async(
        kwargs={
            "later_than": datetime.now() - timedelta(days=365),
            "earlier_than": datetime.now(),
        }
    ).get()  # type: ignore

    if not events:
        message.answer("Пока что нет мероприятий")
        return

    events: list[Event] = [Event.model_validate(event) for event, score in events]  # type: ignore
    await send_events(message, events)


def get_date(event: Event):
    date = event.end_date
    if date is None:
        date = event.start_date
    if date is None:
        date = event.end_registration
    if date is None:
        date = event.start_registration
    return date


async def send_events(message: types.Message, events: list[Event]):
    events = sorted(events, key=get_date, reverse=True)
    for event in events:
        url = "https://codenrock.com/contests/" + str(event.id)
        msg = f"<a href='{url}'>{event.name}</a>\n"
        msg += f"Тип: {event.type}\n"
        if event.tags:
            tags = list(
                map(
                    lambda tag: f"#{tag.name_ru.replace(' ', '_').replace('-', '_').replace('/', ', #')}",
                    event.tags,
                )
            )
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
