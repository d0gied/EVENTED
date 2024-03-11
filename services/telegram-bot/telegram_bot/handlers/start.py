from aiogram import Router, types
from aiogram.filters import Command

from events import events_keyboard

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот для поиска мероприятий."
        "Ниже ты найдешь клавиатуру с фильтрами, которые у меня есть\n"
        "Напиши /help, чтобы узнать, что я умею. ",
        reply_markup=events_keyboard
    )


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(
        "Я могу помочь тебе найти мероприятие по названию, тегу или типу. "
        "Просто напиши мне, что ты ищешь, и я постараюсь помочь тебе.\n"
        "/commands - список команд"
    )


@router.message(Command("commands"))
async def commands(message: types.Message):
    await message.answer(
        "Список команд:\n"
        "/start - начать общение с ботом\n"
        "/help - получить помощь по использованию бота\n"
        "/commands - список команд\n"
        "/events - список всех мероприятий\n"
        "/hackathons - список хакатонов\n"
        "/meetups - список митапов\n"
        "/ai - список мероприятий по тегу AI\n"
        "/week - список мероприятий за последнюю неделю\n"
        "/month - список мероприятий за последний месяц\n"
        "/year - список мероприятий за последний год"
    )
