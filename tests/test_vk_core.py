import unittest
from unittest.mock import patch, MagicMock
from source.vk_core import VKCore
import vk_api


class TestVKCore(unittest.TestCase):
    @patch('vk_api.VkApi.get_api')
    def setUp(self, mock_get_api):
        # Создаем объект VKCore и заменяем вызов VK API на мок-объект
        self.vk_core = VKCore('dummy_token')
        self.mock_api = mock_get_api.return_value

    @patch('vk_api.VkApi.get_api')
    def test_get_profiles_info(self, mock_get_api):
        # Мокируем ответ VK API на запрос профиля пользователя
        self.mock_api.account.getProfileInfo.return_value = {
            'first_name': 'Test',
            'last_name': 'User',
            'city': {'id': 1, 'title': 'TestCity'},
            'bdate': '01.01.2000'
        }

        # Проверяем, что метод возвращает True и корректно заполняет данные пользователя
        result = self.vk_core.get_profiles_info(123456)
        self.assertTrue(result)
        self.assertEqual(self.vk_core.vk_bot_user.first_name, 'Test')
        self.assertEqual(self.vk_core.vk_bot_user.city, 'TestCity')

    @patch('vk_api.VkApi.get_api')
    def test_get_profiles_info_api_error(self, mock_get_api):
        # Проверка обработки ошибки API
        self.mock_api.account.getProfileInfo.side_effect = vk_api.exceptions.ApiError("Error message")
        result = self.vk_core.get_profiles_info(123456)
        self.assertFalse(result)

    def test_get_users_photos(self):
        # Мокируем ответ VK API на запрос фотографий пользователя
        self.mock_api.photos.get.return_value = {
            'items': [
                {'id': 1, 'owner_id': 123, 'likes': {'count': 100}},
                {'id': 2, 'owner_id': 123, 'likes': {'count': 150}},
            ]
        }

        # Проверяем, что метод возвращает список фотографий и сортирует их по лайкам
        photos = self.vk_core.get_users_photos(123)
        self.assertIsNotNone(photos)
        self.assertEqual(len(photos), 2)
        self.assertEqual(photos[0]['likes'], 150)  # Проверка сортировки по лайкам

    def test_get_users_photos_api_error(self):
        # Проверка обработки ошибки при получении фотографий
        self.mock_api.photos.get.side_effect = vk_api.exceptions.ApiError("Error message")
        photos = self.vk_core.get_users_photos(123)
        self.assertIsNone(photos)


if __name__ == '__main__':
    unittest.main()