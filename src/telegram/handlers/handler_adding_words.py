import re

from telebot import formatting

from src.grpc.user_service.user_service import UserService
from src.grpc.word_service.word_service import WordService
from src.log.logger import logger, log_decorator


from src.telegram.handlers.custom_keyboards import hide_keyboard
from src.telegram.handlers.handler_settings import generate_menu
from src.telegram.handlers.telegram_state import TelegramStates
from src.telegram.telegram_decorator import telegram_error_handling
from src.telegram.telegram_const import TelegramConstant


def register_handlers(bot):
    @bot.message_handler(commands=['add_words'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def add_words_process(message):
        """
        Start adding word process for adding new words
        @param message: message information (Get typed words from message)
        @return:
        """
        if UserService.is_user_created(message.chat.username) is False:
            response_str = TelegramConstant.USER_SHOULD_BE_REGISTERED.format(username=formatting.hbold(message.chat.username))
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
        else:
            response_str = TelegramConstant.WORD_PARAMETERS
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            bot.set_state(message.from_user.id, TelegramStates.add_words, message.chat.id)

    @bot.message_handler(commands=['stop_add'])
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def stop_adding_words_process(message):
        """
        Stop adding words
        @param message: message information
        @return:
        """
        response_str = TelegramConstant.SUCCESS_WORDS_TEXT
        bot.send_message(message.chat.id, response_str, generate_menu(), parse_mode='HTML')
        logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
        bot.delete_state(message.from_user.id, message.chat.id)

    @bot.message_handler(state=TelegramStates.add_words)
    @log_decorator(my_logger=logger)
    @telegram_error_handling(bot = bot)
    def add_word(message):
        """
        Add new word to user
        @param message: word information
        @return:
        """
        new_word = message.text
        if not re.match(r"[\w]*[\w]*-*[\w]*[\w]", new_word):
            response_str = (TelegramConstant.VALIDATION_WORD_TEXT)
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
        else:
            words = str(new_word).split('-')
            german_word = words[0]
            russian_word = words[1]
            if (len(words) == 3):
                english_word = words[2]
            else:
                english_word = ""
            WordService.add_new_word(message.chat.username, german_word, english_word, russian_word, 0, 0)
            response_str = (TelegramConstant.SUCCESS_WORD_TEXT)
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
