from src.telegram.gettext_setup import trans
import logging

class MetaTelegramConstant(type):

    # TODO NICE TO HAVE: Add Ability change localisation depends from user
    def __getattribute__(cls, name):
        # Retrieve the attribute value
        attr_value = super().__getattribute__(name)

        # Apply the translation to the value
        if (isinstance(attr_value, dict)):
            translated_dict = {k: trans(v) for k, v in attr_value.items()}
            logging.info(f"Accessing {name}: translated dict is {translated_dict}")
            return translated_dict

        translated_attr = trans(attr_value)
        logging.info(f"Accessing {name}: translated value is '{translated_attr}'")
        return translated_attr

class TelegramConstant(metaclass=MetaTelegramConstant):

    # Telegram buttons
    TRANSLATION = ("Перевод")
    ALREADY_KNOW = ("Помню")
    DONT_KNOW = ("НЕ помню")

    GERMAN_WORD = 'german_word'
    RUSSIAN_WORD = 'russian_word'

    PERCENT_NEW_WORDS_IN_SET = 0.2

    REDIS_TIME_EXPIRED = 360
    REDIS_USER_NAME = 'USER-NAME:'
    REDIS_TOTAL_AMOUNT = 'TOTAL_AMOUNT'
    REDIS_CURRENT_POSITION = 'CURRENT_POSITION'
    REDIS_CURRENT_WORD = 'CURRENT_WORD'
    REDIS_LIST = 'LIST'
    REDIS_LEARNING_SET = 'LEARNING_SET'

    # TEXTs
    FINAL_TEXT = ('Поздравляю! Вы успешно закончили тренировку! Давайте потренируемся еще! /start \n')
    SUCCESS_REGISTRATION_TEXT = ('Ура! Вы были успешно зарегистрированы!')
    VALIDATION_WORD_TEXT = ('Упс, кажется вы неверно ввели слово, которое хотите добавить. Пожалуйста, '
                             'введите его в следующем формате: "german word"-"russian translation-"english translation(optional)"')
    SUCCESS_WORD_TEXT = ('Ура! Вы успешно добавили слово! Продолжайте! '
                         'Введите следующее слова в формате: "german word"-"russian translation-"english translation(optional)"'
                         'Если хотите вернуться к обучению введите /stop_add')
    SUCCESS_WORDS_TEXT = ('Ура! Вы успешно закончили добавление слов! Ура,вы можете вернуться к обучению! /start')

    # Add words
    USER_SHOULD_BE_REGISTERED = ('К сожалению, пользователь с именем {username} не зарегистрирован, '
                                 'пожалуйста, зарегистрируйтесь с помощью кщманды/registration')
    WORD_PARAMETERS = ('Напишите слово, которое хотите добавить на обучение в следующем формате '
                       '"german word"-"russian translation-"english translation(optional)"')

    # learning process
    ALL_LEARNED = ('ВАУ! Кажется вы все выучили! Пожалуйста, добавьте новые слова /add_words или начните сначала /start')
    START_LEARNING_TEXT = ('Привет! Давай потренируемся вместе.\n{currentAmount}/{totalAmount}. Помнишь ли ты слово {current_word}')
    TRANSLATION_TEXT = ('{currentAmount}/{totalAmount}. Текущее слово {current_word} \nПеревод - {word_translation}')
    REMEMBER_WORD_TEXT = ('{currentAmount}/{totalAmount}. Помнишь ли ты слово {new_word}?')

    # Registration
    ENTER_EMAIL = ('Здравствуйте! Давайте потренируем ваш немецкий вместе!'
                    '\n Для этого, вам необходимо зарегистрироваться, пожалуйста, введите вашу почту')
    VALIDATION_EMAIL_TEXT = ('Упс, кажется почта была введена неверно. Подалуйста, попробуйте зарегистрироваться снова! ')
    ALREADY_REGISTERED = "Вы уже зарегистрированы в системе! Вы можете приступить к обучению! /start"

    # Settings
    TRAINING_SET_CHANGED_TEXT = "Длина тренировочного сета была успешно изменена."
    TRAINING_SET_ERR_TEXT = "Возникла ошибка обработки значения. Значение должно быть числом, больше 0."
    TRAINING_SET_QUESTION_TEXT = "Введите новую длину тренировочного сета."


    # Menu
    ACTIONS_TEXT = ("Вот список всех возможных команд:")
    COMMANDS = {
        "/start": ("Начать обучение."),
        "/learn_standard_words": ("Изучить стандартные слова."),
        "/learn_user_words": ("Изучить словаб добавленные Вами."),
        "/help": ("Получить список всех доступных команд."),
        "/registration": ("Зарегистрироваться."),
        "/add_words": ("Добавить новые слова."),
        "/stop_add": ("Закончить процесс добавления слов."),
        "/settings": ("Перейти к настройкам")
    }

    # Settings
    SETTINGS_TEXT = ("Вот список всех возможных команд:")
    SETTINGS_COMMANDS = {
        "/change_training_length": ("Изменить длину изучающего сета"),
        "/select_level": ("Выбрать уровень языка, для стандартной тренировки")
    }

    # Language
    CHANGE_LANGUAGE = "Хотите сменить язык?"
    CHANGED_TO_EN = "Язык изменен на EN"
    CHANGED_TO_RU = "Язык изменен на RU"