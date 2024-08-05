from telebot.types import ReplyKeyboardRemove, ReplyKeyboardMarkup
from src.telegram.telegram_const import TelegramConstant
from telebot import types

def generate_full_learning_keyboard() -> ReplyKeyboardMarkup:
    """
    Generate menu for learning process
    @return: ReplyKeyboardMarkup with 3 options
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    translation = types.KeyboardButton(TelegramConstant.TRANSLATION)
    already_know = types.KeyboardButton(TelegramConstant.ALREADY_KNOW)
    to_education = types.KeyboardButton(TelegramConstant.DONT_KNOW)
    markup.add(translation, already_know, to_education)
    return markup

def generate_translation_keyboard() -> ReplyKeyboardMarkup:
    """
    Generate menu for learning process (without translation button)
    @return: ReplyKeyboardMarkup with 2 options
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)

    already_know = types.KeyboardButton(TelegramConstant.ALREADY_KNOW)
    to_education = types.KeyboardButton(TelegramConstant.DONT_KNOW)
    markup.add( already_know, to_education)
    return markup

def generate_language_keyboard() -> ReplyKeyboardMarkup:
    """
    Generate menu for learning process (without translation button)
    @return: ReplyKeyboardMarkup with 2 options
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    en = types.KeyboardButton("/en")
    ge = types.KeyboardButton("/ru")
    markup.add( en, ge)
    return markup

def hide_keyboard() -> ReplyKeyboardRemove:
    """
    Hide keyboard
    @return:ReplyKeyboardRemove
    """
    markup = types.ReplyKeyboardRemove()
    return markup
