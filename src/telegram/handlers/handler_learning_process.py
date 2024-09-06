from telebot import formatting

from src.grpc.process_service.process_service import ProcessService
from src.grpc.user_service.user_service import UserService
from src.log.logger import logger, log_decorator

from src.model.user_action_enum import UserActionEnum
from src.model.word_type_enum import WordTypeEnum
from src.telegram.handlers.custom_keyboards import hide_keyboard, generate_full_learning_keyboard, \
    generate_translation_keyboard
from src.telegram.handlers.handler_settings import generate_menu
from src.telegram.handlers.telegram_state import TelegramStates
from src.telegram.telegram_decorator import telegram_error_handling
from src.telegram.telegram_const import TelegramConstant

def register_handlers(bot):

    # ------------------LEARNING WITH STANDARD WORDS------------------
    @bot.message_handler(commands=['start','learn_standard_words'])
    @log_decorator(my_logger=logger)
    # @telegram_error_handling(bot = bot)
    def start_standard_words(message):
        """
        Start learning process with standard words
        @param message: message information
        @return:
        """
        # Start learning process with Custom words
        start_learning_process(message, WordTypeEnum.standard)

    @bot.message_handler(state=TelegramStates.standard_learning_process)
    @log_decorator(my_logger=logger)
    # @telegram_error_handling(bot = bot)
    def standard_learning_process(message):
        """
        Continue standard learning process
        Recognise it by state - standard_learning_process
        @param message:
        @return:
        """
        learning_iteration(message, WordTypeEnum.standard)

    # ------------------LEARNING WITH CUSTOM WORDS------------------
    @bot.message_handler(commands=['learn_user_words'])
    @log_decorator(my_logger=logger)
    # @telegram_error_handling(bot = bot)
    def start_learning_user_words(message):
        """
        Start learning process with standard words
        @param message: message information
        @return:
        """

        # Start learning process with Custom words
        start_learning_process(message, WordTypeEnum.custom)

    @bot.message_handler(state=TelegramStates.custom_learning_process)
    @log_decorator(my_logger=logger)
    # @telegram_error_handling(bot = bot)
    def custom_learning_process(message):
        """
        Continue standard learning process
        Recognise it by state - standard_learning_process
        @param message:
        @return:
        """
        learning_iteration(message, WordTypeEnum.custom)

    # ------------------LEARNING PROCESS------------------
    def start_learning_process(message, word_type: WordTypeEnum):
        # if user is not in a system - ask user for registration
        if UserService.is_user_created(message.chat.username) is False:
            response_str = TelegramConstant.USER_SHOULD_BE_REGISTERED.format(
                username=formatting.hbold(message.chat.username))
            bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
        else:
            learning_set = ProcessService.start_learning_process(message.chat.username, word_type)
            current_word = learning_set.get_current_word().german_word

            response_str = TelegramConstant.START_LEARNING_TEXT.format(currentAmount=learning_set.get_current_position(),
                                                                       totalAmount=learning_set.get_total_length(),
                                                                       current_word=formatting.hbold(current_word))
            # Set up learning state
            if (word_type == word_type.standard):
                bot.set_state(message.from_user.id, TelegramStates.standard_learning_process, message.chat.id)
            else:
                bot.set_state(message.from_user.id, TelegramStates.custom_learning_process, message.chat.id)
            bot.send_message(message.chat.id, response_str, parse_mode='HTML',
                             reply_markup=generate_full_learning_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

    def learning_iteration(message, word_type: WordTypeEnum):
        learning_set = ProcessService.get_learning_set(message.chat.username, word_type)
        currentAmount = learning_set.get_current_position()
        totalAmount = learning_set.get_total_length()
        current_word = learning_set.get_current_word()

        if (learning_set.get_current_position() < learning_set.get_total_length()):
            if message.text == TelegramConstant.TRANSLATION:
                response_str = TelegramConstant.TRANSLATION_TEXT.format(currentAmount=currentAmount,
                                                                        totalAmount=totalAmount,
                                                                        current_word=current_word.german_word,
                                                                        word_translation=formatting.hbold(current_word.russian_word))
                bot.send_message(message.chat.id, response_str, parse_mode='HTML',
                                 reply_markup=generate_translation_keyboard())
                logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            elif message.text == TelegramConstant.ALREADY_KNOW:
                # Update information about word which just user learned
                ProcessService.update_learning_progress(user_id=learning_set.user.id,
                                                        word_id=current_word.id,
                                                        german_word=current_word.german_word,
                                                        user_action=UserActionEnum.ALREADY_KNOW,
                                                        word_type=word_type)
                # Get next word
                word = learning_set.get_next_word()
                if (word is None):
                    response_str = TelegramConstant.ALL_LEARNED
                    bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
                    logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
                else:
                    new_word = word.german_word
                    # Get actual amount
                    currentAmount = learning_set.get_current_position()
                    response_str = TelegramConstant.REMEMBER_WORD_TEXT.format(currentAmount=currentAmount,
                                                                              totalAmount=totalAmount,
                                                                              new_word=formatting.hbold(new_word))
                    bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=generate_full_learning_keyboard())
                    logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
            elif message.text == TelegramConstant.DONT_KNOW:
                # Update learning process
                ProcessService.update_learning_progress(user_id=learning_set.user.id,
                                                        word_id=current_word.id,
                                                        german_word=current_word.german_word,
                                                        user_action=UserActionEnum.BACK_TO_LEARNING,
                                                        word_type=word_type)
                # Get next word
                word = learning_set.get_next_word()
                if (word is None):
                    # TODO: change condition
                    response_str = TelegramConstant.ALL_LEARNED
                    bot.send_message(message.chat.id, response_str, parse_mode='HTML', reply_markup=hide_keyboard())
                    logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")
                else:
                    new_word = word.german_word
                    # Get actual amount
                    currentAmount = learning_set.get_current_position()
                    response_str = TelegramConstant.REMEMBER_WORD_TEXT.format(currentAmount=currentAmount,
                                                                              totalAmount=totalAmount,
                                                                              new_word=formatting.hbold(new_word))
                    bot.send_message(message.chat.id, response_str, parse_mode='HTML',
                                     reply_markup=generate_full_learning_keyboard())
                    logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

        else:
            response_str = TelegramConstant.FINAL_TEXT
            # TODO: NEED TO HAVE ABILITE SHOW TRANSLATION HERE SOMEHOW
            # Save Last iteration
            if message.text == TelegramConstant.ALREADY_KNOW:
                ProcessService.update_learning_progress(user_id=learning_set.user.id,
                                                        word_id=current_word.id,
                                                        german_word=current_word.german_word,
                                                        user_action=UserActionEnum.ALREADY_KNOW,
                                                        word_type=word_type)
            elif message.text == TelegramConstant.DONT_KNOW:
                # Update learning process
                ProcessService.update_learning_progress(user_id=learning_set.user.id,
                                                        word_id=current_word.id,
                                                        german_word=current_word.german_word,
                                                        user_action=UserActionEnum.BACK_TO_LEARNING,
                                                        word_type=word_type)
            bot.delete_state(message.from_user.id, message.chat.id)
            bot.send_message(message.chat.id, response_str, reply_markup=hide_keyboard())
            bot.send_message(message.chat.id, generate_menu(), reply_markup=hide_keyboard())
            logger.debug(f"To ChatId: {message.chat.id} was sent message: {response_str} ")

        # Update learning set in Redis
        ProcessService.add_learning_set_to_cash(learning_set)
