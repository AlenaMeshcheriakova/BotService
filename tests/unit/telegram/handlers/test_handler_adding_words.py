import pytest
from unittest.mock import MagicMock, patch

from src.telegram.handlers import handler_adding_words

from tests.unit.test_data_preparation import (DataPreparation, mock_bot)

class TestAddingWordProcess:
    """Group of Unit-Tests for telegram handlers in handler_adding_words"""

    @pytest.fixture
    def mock_message(self):
        """Fixture to create a mock message."""
        message = MagicMock()
        message.chat.username = DataPreparation.TEST_USER_NAME
        message.chat.id = '123456'
        message.from_user.id = DataPreparation.TEST_USER_ID
        message.text = "GermanWord-RussianWord"
        return message

    # @pytest.fixture
    # def mock_user_service(self):
    #     """Fixture to mock UserService."""
    #     with patch('src.service.user_service.UserService') as mock:
    #         yield mock


    # @pytest.fixture
    # def mock_word_service(self):
    #     """Fixture to mock UserService."""
    #     with patch('src.service.word_service.WordService') as mock:
    #         yield mock


    @pytest.fixture
    def mock_telegram_constants(self):
        """Fixture to mock TelegramConstant."""
        with patch('src.telegram.telegram_const.TelegramConstant') as mock:
            yield mock


    @pytest.fixture
    def mock_log_decorator(self):
        """Fixture to mock log_decorator."""
        with patch('src.log.logger.log_decorator') as mock:
            yield mock


    @pytest.fixture
    def mock_hide_keyboard(self):
        """Fixture to mock hide_keyboard function."""
        with patch('src.telegram.handlers.custom_keyboards.hide_keyboard') as mock:
            yield mock


    @pytest.fixture
    def mock_telegram_states(self):
        """Fixture to mock TelegramStates."""
        with patch('src.telegram.handlers.telegram_state.TelegramStates') as mock:
            yield mock


    def test_add_words_process_user_registered(
            self, mock_bot, mock_message, mock_telegram_constants,
            mock_log_decorator, mock_hide_keyboard, mock_telegram_states
    ):
        # TODO: Rewrite TEST with mocking grpc
        """Test the add_words_process when user is not registered."""

        # # Mock UserService response
        # mock_user_service.is_user_created.return_value = False

        # Mock TelegramConstant responses
        mock_telegram_constants.USER_SHOULD_BE_REGISTERED = "User should be registered {username}"
        mock_telegram_constants.WORD_PARAMETERS = "Please provide the words."

        # Mock log_decorator to just return the function
        mock_log_decorator.return_value = lambda f: f

        # Register the handlers
        handler_adding_words.register_handlers(mock_bot)

        # Call the add_words_process function
        handler = mock_bot.message_handler('/add_words').call_args[0][0]
        handler(mock_message)

        # Assert that bot.send_message was called with the correct parameters
        test_str_res = ('Hooray! You have successfully added the word! Keep going! '
                        'Enter the next word in the format: '
                        '"german word"-"russian translation-"english translation(optional)" '
                        'If you want to return to training, enter /stop_add')

        assert mock_bot.send_message.call_count == 1
        assert mock_bot.send_message.call_args[0][0] == mock_message.chat.id
        assert mock_bot.send_message.call_args[0][1] == test_str_res

