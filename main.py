from aiogram import executor, Bot, Dispatcher, types
from bot_tocken import BOT_TOCKEN
import asyncio

loop = asyncio.get_event_loop()
bot = Bot(BOT_TOCKEN, parse_mode='HTML')

dp = Dispatcher(bot, loop=loop)


if __name__ == '__main__':
    from handlers import dp, send_to_admin
    executor.start_polling(dp, on_startup=send_to_admin)