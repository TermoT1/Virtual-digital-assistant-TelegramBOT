import logging
from aiogram import Bot, Dispatcher
#Для хранения в памяти
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#Логгирование
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.BOT_TOKEN:
    exit("No token provided")

# init
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
#storage=MemoryStorage() для хранения в памяти states
dp = Dispatcher(bot, storage=MemoryStorage())
#Логгирование
dp.middleware.setup(LoggingMiddleware())

# activate filters
dp.filters_factory.bind(IsOwnerFilter)
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(MemberCanRestrictFilter)
