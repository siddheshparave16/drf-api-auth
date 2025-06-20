import logging
from telegram.ext import ApplicationBuilder

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.application = None

    def start(self):
        """Initialize and start the bot."""
        try:
            from .bot_handlers import setup_application
            logger.info("Setting up Telegram bot application")
            self.application = setup_application()
            logger.info("Starting bot polling")
            self.application.run_polling(drop_pending_updates=True)
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise