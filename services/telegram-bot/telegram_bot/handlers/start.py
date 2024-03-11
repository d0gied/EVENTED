from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я бот для поиска мероприятий. Напиши /help, чтобы узнать, что я умею."
    )


@router.message(Command("help"))
async def help(message: types.Message):
    await message.answer(
        "Я могу помочь тебе найти мероприятие по названию, тегу или типу. "
        "Просто напиши мне, что ты ищешь, и я постараюсь помочь тебе."
        "Также ты можешь посмотреть предстоящие мероприятия, написав /events."
    )
