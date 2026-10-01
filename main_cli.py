import asyncio
import logging
from src.core.bot_engine import TelegramMonitorBot

if __name__ == "__main__":
    bot = TelegramMonitorBot()
    asyncio.run(bot.start())
