from datetime import datetime

from aiogram import Bot
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict


def date_fmt(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


async def poll_events(bot: Bot):
    events: list[tuple[EventDict, int]] = IDatabase.new_events.apply_async().get()  # type: ignore
    if not events:
        return

    for event in events:
        await send_event(bot, event)  # type: ignore


async def send_event(bot: Bot, event: EventDict):  # type: ignore
    event: Event = Event.model_validate(event)  # type: ignore

    subscribers = []
    for tag in event.tags:
        tag = tag.name_ru
        subscribers += IDatabase.subscribers.apply_async(kwargs={"tag": tag}).get()  # type: ignore

    subscribers = list(set(subscribers))
    for user_id in subscribers:
        await send_user_event(bot, user_id, event)


async def send_user_event(bot: Bot, user_id: int, event: Event):
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
        await bot.send_photo(user_id, image, caption=msg, parse_mode="HTML")
    else:
        await bot.send_message(user_id, msg, parse_mode="HTML")
