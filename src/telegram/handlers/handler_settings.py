from src.grpc.user_service.user_service import UserService
from src.log.logger import log_decorator, logger

from src.telegram.gettext_setup import active_translation
from src.telegram.handlers.custom_keyboards import hide_keyboard, generate_language_keyboard
from src.telegram.handlers.telegram_state import TelegramStates
from src.telegram.telegram_decorator import telegram_error_handling
from src.telegram.telegram_const import TelegramConstant

def generate_menu() -> str:
    """
    Generate a Menu list actions
    @return: srt with info with all actions
    """
    response = (TelegramConstant.ACTIONS_TEXT) + "\n\n"
    commands = TelegramConstant.COMMANDS
    for command, description in commands.items():
        response += f"{command}: {(description)}\n"
    return response

def generate_settings() -> str:
    """
    Generate a Setting list actions
    @return: srt with info with all actions
    """
    response = (TelegramConstant.SETTINGS_TEXT) + "\n\n"
    commands = TelegramConstant.SETTINGS_COMMANDS
    for command, description in commands.items():
        response += f"{command}: {(description)}\n"
    return response


def register_handlers(bot):
    @bot.message_handler(commands=['/', 'help'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def send_settings(message):
        """
        Send list of actions in Bot (MENU)
        @param message: message information
        @return: list of actions
        """
        response_str = generate_menu()
        bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(commands=['settings'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def send_settings(message):
        """
        Allowed user some settings change
        @param message: message information
        @return: list of settings
        """
        response_str = generate_settings()
        bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(commands=['change_training_length'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def ask_new_training_length(message):
        """
        Set new change training length
        @param message: New training length value
        @return: response and activity list
        """
        response_str = TelegramConstant.TRAINING_SET_QUESTION_TEXT
        bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
        bot.set_state(message.from_user.id, TelegramStates.training_length, message.chat.id)
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(state=TelegramStates.training_length)
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def get_chat_id(message):
        """
        Allowed user change length of the training set
        By default = 10
        @param message: message information
        @return: User chat ID
        """
        try:
            new_training_length = int(message.text)
            if (new_training_length < 0):
                raise ValueError(f"Value of new_training_length is less than 0: {new_training_length}")

            # Change training length
            UserService.update_user_training_length(message.chat.username, new_training_length)
            response_str = TelegramConstant.TRAINING_SET_CHANGED_TEXT
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
            bot.send_message(message.chat.id, generate_menu(), reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

        except Exception as ex:
            response_err_str = TelegramConstant.TRAINING_SET_ERR_TEXT
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, response_err_str, reply_markup=hide_keyboard())
            bot.send_message(message.chat.id, generate_menu(), reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_err_str} ")


    @bot.message_handler(commands=['get_chat_id'])
    @log_decorator(my_logger=CustomLogger())
    @telegram_error_handling(bot = bot)
    def get_chat_id(message):
        """
        Send user chat ID
        @param message: message information
        @return: User chat ID
        """
        response_str = message.chat.id
        bot.send_message(message.chat.id, message.chat.id, reply_markup=hide_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(commands=['language'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def change_language(message):
        """
        Change language for user
        @param message: message information
        @return: None
        """
        response_str = TelegramConstant.CHANGE_LANGUAGE
        bot.send_message(message.chat.id, response_str, reply_markup=generate_language_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(commands=['en'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def change_language_eu(message):
        """
        Change language to EU
        @param message: message information
        @return: None
        """
        active_translation('en_US')
        response_str = TelegramConstant.CHANGED_TO_EU, generate_menu()
        bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    @bot.message_handler(commands=['ru'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def change_language_ru(message):
        """
        Change language to RU
        @param message: message information
        @return: None
        """
        active_translation('ru_RU')
        response_str = TelegramConstant.CHANGED_TO_RU, generate_menu()
        bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")