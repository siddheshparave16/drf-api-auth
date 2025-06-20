from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler
from .models import TelegramUser
from django.db import connection
from django.db.models import Q
from asgiref.sync import sync_to_async

class SecretsFilter(logging.Filter):
    """Filter to redact sensitive information from logs"""
    def __init__(self):
        self.secrets = [
            os.getenv("TELEGRAM_BOT_TOKEN"),
            os.getenv("DB_PASSWORD"),
            os.getenv("EMAIL_HOST_PASSWORD")
        ]
        
    def filter(self, record):
        if isinstance(record.msg, str):
            for secret in self.secrets:
                if secret and secret in record.msg:
                    record.msg = record.msg.replace(secret, "[REDACTED]")
        return True

def configure_logging():
    """Production-grade logging setup"""
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Main logger configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Add filter to all handlers
    secrets_filter = SecretsFilter()
    
    # Console handler (for systemd/journald)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.addFilter(secrets_filter)
    logger.addHandler(console_handler)
    
    # File handler (rotated logs)
    file_handler = RotatingFileHandler(
        filename='bot.log',
        maxBytes=5*1024*1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.addFilter(secrets_filter)
    logger.addHandler(file_handler)
    
    # Configure third-party loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)

def setup_application():
    # Initialize logging first
    configure_logging()
    logger = logging.getLogger(__name__)
    
    # Load environment variables
    load_dotenv()
    API_KEY = os.getenv("TELEGRAM_BOT_TOKEN")
    if not API_KEY:
        logger.critical("TELEGRAM_BOT_TOKEN not found in environment variables")
        raise ValueError("Missing bot token")
    
    # Database connection check
    try:
        connection.ensure_connection()
        logger.info("Database connection established")
    except Exception as e:
        logger.critical("Database connection failed", exc_info=True)
        raise

    @sync_to_async
    def save_user_to_db(user):
        """Synchronous function to save user"""
        if not user.username and not user.first_name:
            logger.warning("Incomplete user data received")
            return None

        try:
            # Get or create user
            obj, created = TelegramUser.objects.get_or_create(
                telegram_id=user.id,
                defaults={
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'username': user.username
                }
            )
            
            # If user exists, just update active_at (auto_now=True handles the timestamp)
            if not created:
                obj.save(update_fields=['active_at'])  # Only updates active_at field
                
            return obj, created
        
        except Exception as e:
            logger.error("Failed to save user", exc_info=True)
            raise

    async def save_user(user):
        """Async wrapper for user saving"""
        try:
            obj, created = await save_user_to_db(user)
            if obj:
                logger.info(
                    "User %s: %s",
                    "created" if created else "exists",
                    user.username or user.id
                )
            return obj
        except Exception as e:
            logger.error("User save operation failed", exc_info=True)
            return None

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        logger.info(f"Received /start command from user: {update.effective_user.id}")
        user = update.effective_user
        if not user:
            logger.error("Effective user is None.")
            await update.message.reply_text("Could not retrieve your user information.")
            return

        logger.info(f"Bot started by user: {user}")
        await save_user(user)

        response = f"Hi @{user.username}, thank you for participating in the survey." if user.username else (
            f"Hi {user.first_name}! (ID: {user.id})\n"
            "You can set a username in Telegram settings."
        )
        await update.message.reply_text(response)

    async def exit_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /exit command."""
        logger.debug("Handling /exit command.")
        await update.message.reply_text("Goodbye! Type /start to begin again.")

    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        logger.debug("Handling /help command.")
        help_text = (
            "We are conducting a survey of Telegram users who interact with us.\n"
            "We store your activity online along with your name, username, and last name."
        )
        await update.message.reply_text(help_text)

    async def unknown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands."""
        logger.debug("Handling unknown command.")
        await update.message.reply_text(
            "Please use one of these commands:\n"
            "/start - Begin interaction\n"
            "/help - Get information\n"
            "/exit - End session"
        )

    async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
        """Log the error and notify the user."""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.message:
            await update.message.reply_text("An error occurred. Please try again later.")

    app = ApplicationBuilder().token(API_KEY).build()

    # Set bot commands
    async def post_init(application):
        logger.debug("Setting bot commands.")
        await application.bot.set_my_commands([
            ("start", "Start interaction with bot"),
            ("exit", "Exit the bot"),
            ("help", "Get bot information"),
        ])

    app.post_init = post_init

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("exit", exit_command))
    app.add_handler(CommandHandler("help", help_command))

    # Handle unrecognized commands and messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_command))
    app.add_handler(MessageHandler(filters.COMMAND, unknown_command))

    # Error handler
    app.add_error_handler(error_handler)

    return app
