from aiogram import Bot, Dispatcher, types
from telegram_bot.config import TelegramConfig
from telegram_bot.handlers.events import router as events_router
from telegram_bot.handlers.search import router as search_router
from telegram_bot.handlers.start import router as start_router

routers = [events_router, start_router, search_router]

config = TelegramConfig()


dp = Dispatcher()

for router in routers:
    dp.include_router(router)
    print(f"Include router {router.__class__.__name__}")


async def main():
    bot = Bot(token=config.token.get_secret_value())
    bot_name = (await bot.get_me()).username

    print(f"Start bot https://t.me/{bot_name}")
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
