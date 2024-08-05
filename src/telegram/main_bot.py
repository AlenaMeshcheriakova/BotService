
from cfg.сonfig import settings

# telebot - library pyTelegramBotAPI
import telebot

# States storage
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

from src.log.logger import CustomLogger
from src.telegram.gettext_setup import active_translation

# Initialisation telegram storage
state_storage = StateMemoryStorage()
# Initialise telegram bot
bot = telebot.TeleBot(settings.BOT_TOKEN, state_storage=state_storage)

# Add handlers
from src.telegram.handlers import (handler_settings, handler_registration,
                                   handler_adding_words, handler_learning_process)

def setup_handlers():
    """
    Register all handlers
    """
    handler_registration.register_handlers(bot)
    handler_settings.register_handlers(bot)
    handler_adding_words.register_handlers(bot)
    handler_learning_process.register_handlers(bot)

if __name__ == "__main__":
    # Ensure gettext is set up before accessing constants
    active_translation('ru_RU')

    # Add Handlers
    setup_handlers()

    # Initialize custom logger
    logger_instance = CustomLogger()
    logger = logger_instance.get_logger(__name__)
    logger.info("Bot is starting...")

    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()



