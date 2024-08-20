import unittest
from unittest.mock import patch, MagicMock
from database.db_vkbot import DBManager
from models.vk_user import VKUser
from sqlalchemy.exc import IntegrityError


class TestDBManager(unittest.TestCase):
    @patch('database.db_vkbot.Session')
    def setUp(self, mock_session):
        # Создаем объект DBManager и мокируем сессию базы данных
        self.db_manager = DBManager()
        self.mock_session = mock_session.return_value

    def test_insert_vk_user(self):
        # Проверка вставки нового пользователя в базу данных
        vk_user = VKUser(id=1, first_name="Test", last_name="User")
        self.mock_session.commit = MagicMock()

        result = self.db_manager.insert_vk_user(vk_user)

        # Убедимся, что пользователь был добавлен и commit был вызван
        self.mock_session.add.assert_called_once_with(vk_user)
        self.mock_session.commit.assert_called_once()
        self.assertTrue(result)

    def test_insert_vk_user_duplicate(self):
        # Проверка обработки ошибки вставки дубликата
        self.mock_session.commit.side_effect = IntegrityError("Duplicate", "params", "orig")
        vk_user = VKUser(id=1, first_name="Test", last_name="User")
        result = self.db_manager.insert_vk_user(vk_user)
        self.assertFalse(result)

    def test_select_vk_user(self):
        # Проверка выборки пользователя из базы данных
        mock_user = VKUser(id=1, first_name="Test", last_name="User")
        self.mock_session.execute.return_value.scalars.return_value.first.return_value = mock_user
        user = self.db_manager.select_vk_user(1)
        # Убедимся, что вернулся правильный пользователь
        self.assertIsNotNone(user)
        self.assertEqual(user.first_name, "Test")


if __name__ == '__main__':
    unittest.main()
