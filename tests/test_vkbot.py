import unittest
from unittest.mock import patch, MagicMock
from source.vk_bot_main import VKBot
from vk_api.longpoll import VkEventType

class TestVKBot(unittest.TestCase):
    @patch('source.vk_bot_func.VKBotFunc.starting_actions')
    def setUp(self, mock_starting_actions):
        # Создаем объект VKBot и мокируем его функции
        self.vk_bot = VKBot()
        self.mock_starting_actions = mock_starting_actions

    @patch('source.vk_bot_func.VKBotFunc.send_msg')
    def test_pressed_start(self, mock_send_msg):
        # Проверка обработки команды START
        event = MagicMock()
        event.user_id = 123
        self.vk_bot.pressed_start(event)
        self.mock_starting_actions.assert_called_once_with(123)
        mock_send_msg.assert_called_once()

    @patch('source.vk_bot_func.VKBotFunc.send_msg')
    def test_pressed_hello(self, mock_send_msg):
        # Проверка обработки команды HELLO
        event = MagicMock()
        event.user_id = 123
        self.vk_bot.pressed_hello(event)
        mock_send_msg.assert_called_with(123, 'Привет, 123')

if __name__ == '__main__':
    unittest.main()
