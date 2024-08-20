import unittest
from keyboards.keyboard import Keyboard
from vk_api.keyboard import VkKeyboardColor

class TestKeyboard(unittest.TestCase):
    def setUp(self):
        # Создаем объект Keyboard для каждого теста
        self.keyboard = Keyboard()

    def test_get_keyboards(self):
        # Проверка создания основной клавиатуры
        keyboard = self.keyboard.get_keyboards(['Button1', 'Button2'])
        self.assertIn('Button1', keyboard)
        self.assertIn('Button2', keyboard)

    def test_get_inline_keyboards(self):
        # Проверка создания inline-клавиатуры
        user = {'id': 1, 'first_name': 'Test', 'last_name': 'User'}
        keyboard = self.keyboard.get_inline_keyboards(user, ['Button1', 'Button2'])
        self.assertIn('add_to_blacklist', keyboard)
        self.assertIn('add_to_favorite', keyboard)

    def test_get_settings_keyboard(self):
        # Проверка создания клавиатуры настроек
        keyboard = self.keyboard.get_settings_keyboard(
            user_id=1,
            buttons_titles=['Button1', 'Button2'],
            actions=['action1', 'action2']
        )
        self.assertIn('Button1', keyboard)
        self.assertIn('action1', keyboard)

if __name__ == '__main__':
    unittest.main()
