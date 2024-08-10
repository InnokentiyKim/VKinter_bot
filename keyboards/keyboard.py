from vk_api.keyboard import  VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self):
        self.keyboard = VkKeyboard()
        self.keyboard.add_button('Начать', color=VkKeyboardColor.SECONDARY)
        self.keyboard.add_button('Инструкция', color=VkKeyboardColor.SECONDARY)

    def get_keyboard(self):
        return self.keyboard.get_keyboard()