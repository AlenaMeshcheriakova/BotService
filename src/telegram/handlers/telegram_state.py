from telebot.handler_backends import State, StatesGroup


class TelegramStates(StatesGroup):
    """
    Create state objects for Chat sequencing
    """
    basic = State()
    e_mail = State()
    name = State()
    password = State()
    add_words = State()
    training_length = State()
    standard_learning_process = State()
    custom_learning_process = State()