import unittest
from unittest.mock import patch, MagicMock
from source.vk_bot_func import VKBotFunc

class TestVKBotFunc(unittest.TestCase):
    @patch('vk_api.VkApi.method')
    def setUp(self, mock_method):
        # Создаем объект VKBotFunc и мокируем метод VK API
        self.bot_func = VKBotFunc()
        self.mock_method = mock_method

    def test_send_chat_msg(self):
        # Проверка отправки сообщения в чат
        self.bot_func.send_chat_msg(1, "Test Message")
        self.mock_method.assert_called_with('messages.send', {
            'chat_id': 1,
            'message': 'Test Message',
            'random_id': unittest.mock.ANY
        })

    def test_find_next_suitable_profile(self):
        # Мокируем пользователей и черный список
        self.bot_func.found_users = [
            {'id': 1, 'relation': 5, 'is_closed': False},
            {'id': 2, 'relation': 1, 'is_closed': False}
        ]
        self.bot_func.current_user = MagicMock()
        self.bot_func.current_user.blacklist = []

        # Проверяем, что нашелся подходящий пользователь
        result = self.bot_func._find_next_suitable_profile(self.bot_func.found_users)
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], 2)

    @patch('source.vk_bot_func.VKCore.get_profiles_info')
    def test_starting_actions(self, mock_get_profiles_info):
        # Проверка начальных действий при старте поиска
        mock_get_profiles_info.return_value = True
        self.bot_func.starting_actions(1)
        self.assertEqual(self.bot_func.found_person_index, -1)

if __name__ == '__main__':
    unittest.main()
