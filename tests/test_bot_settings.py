import unittest
from source.vk_bot_core import BotSettings

class TestBotSettings(unittest.TestCase):
    def setUp(self):
        # Создаем объект BotSettings для каждого теста
        self.bot_settings = BotSettings()

    def test_initial_settings(self):
        # Проверка начальных значений настроек
        self.assertEqual(self.bot_settings.age_from, 20)
        self.assertEqual(self.bot_settings.age_to, 22)
        self.assertTrue(self.bot_settings.use_blacklist)

    def test_age_range_correction(self):
        # Проверка корректировки возрастных ограничений
        self.bot_settings.correct_age_range()

        # Минимальный возраст не должен быть меньше 16, максимальный не больше 60
        self.assertGreaterEqual(self.bot_settings.age_from, 16)
        self.assertLessEqual(self.bot_settings.age_to, 60)

    def test_switch_blacklist(self):
        # Проверка переключения использования черного списка
        self.bot_settings.switch_use_blacklist()
        self.assertFalse(self.bot_settings.use_blacklist)
        self.bot_settings.switch_use_blacklist()
        self.assertTrue(self.bot_settings.use_blacklist)

if __name__ == '__main__':
    unittest.main()
