from vk_api.keyboard import  VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self):
        self.keyboard = VkKeyboard()

    def get_keyboard(self, title: str, color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        self.keyboard.add_button(label=title, color=color)
        return self.keyboard.get_keyboard()

    def get_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        for button in buttons_titles:
            self.keyboard.add_button(label=button, color=color)
        return self.keyboard.get_keyboard()
