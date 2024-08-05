import re

from src.grpc.user_service.user_service import UserService
from src.log.logger import CustomLogger, log_decorator

from src.telegram.handlers.custom_keyboards import hide_keyboard
from src.telegram.telegram_decorator import telegram_error_handling
from src.telegram.telegram_const import TelegramConstant
from src.telegram.handlers.telegram_state import TelegramStates

# Custom logger
logger = CustomLogger().get_logger(__name__)
def register_handlers(bot):

    @bot.message_handler(commands=['registration'])
    @log_decorator(my_logger=CustomLogger())
    @telegram_error_handling(bot = bot)
    def create_login_pass(message):
        """
        User have to be registered in the system for learning
        @param message: message information
        @return: Sending message - continue registration (input email)
        """
        # TODO CRIT: That user didn't have an account
        is_user_created = UserService.is_user_created(message.chat.username)
        if (is_user_created):
            response_str = TelegramConstant.ALREADY_REGISTERED
            bot.send_message(message.chat.id, response_str , parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
        else:
            response_str = TelegramConstant.ENTER_EMAIL
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            bot.set_state(message.from_user.id, TelegramStates.e_mail, message.chat.id)

    @bot.message_handler(state=TelegramStates.e_mail)
    @log_decorator(my_logger=CustomLogger())
    @telegram_error_handling(bot = bot)
    def message_reply_email(message):
        """
        Registration - entering email
        @param message: message information (get user emeil)
        @return:
        """
        email = message.text
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            response_str = (TelegramConstant.VALIDATION_EMAIL_TEXT)
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            bot.delete_state(message.from_user.id, message.chat.id)
        else:
            UserService.create_user(message.chat.username, email, message.chat.id, message.chat.id)
            response_str = (TelegramConstant.SUCCESS_REGISTRATION_TEXT)
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            bot.delete_state(message.from_user.id, message.chat.id)
