from django.core.management.base import BaseCommand
from securegate.telegrambot import TelegramBot
import logging
import time
from django.db import connection


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        logger.info("Starting Telegram bot...")
        bot = TelegramBot()
        
        try:
            bot.start()
            # Keep the process alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Stopping Telegram bot...")
        except Exception as e:
            logger.error(f"Bot failed: {e}")
            raise
        finally:
            connection.close()  # Cleanup DB connections