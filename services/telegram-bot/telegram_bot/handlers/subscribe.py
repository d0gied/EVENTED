from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.filters import Command
from common_utils.database import IDatabase
from common_utils.models.event import Event, EventDict

from .events import send_events

router = Router()


def date_fmt(date: datetime) -> str:
    return date.strftime("%d.%m.%Y %H:%M")


@router.message(Command("/subscribe"))
async def subscribe(message: types.Message):
    IDatabase.subscribe.apply_async(kwargs={"user_id": message.from_user.id}).get()  # type: ignore
    await message.answer("Вы подписаны на обновления")


@router.message(Command("/unsubscribe"))
async def unsubscribe(message: types.Message):
    IDatabase.unsubscribe.apply_async(kwargs={"user_id": message.from_user.id}).get()  # type: ignore
    await message.answer("Вы отписаны от обновлений")
