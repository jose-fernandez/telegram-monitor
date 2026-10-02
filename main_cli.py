import asyncio
import logging
from src.core.bot_engine import TelegramMonitorBot

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    bot = TelegramMonitorBot()
    asyncio.run(bot.start())
