from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self):
        self.keyboard = VkKeyboard()
        self.inline_keyboard = VkKeyboard()

    def get_keyboard(self, title: str, color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        self.keyboard.add_button(label=title, color=color)
        return self.keyboard.get_keyboard()

    def get_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        for button in buttons_titles:
            self.keyboard.add_button(label=button, color=color)
        return self.keyboard.get_keyboard()

    def get_inline_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        self.inline_keyboard.one_time = one_time
        self.inline_keyboard.inline = True
        if len(buttons_titles) == 2:
            self.inline_keyboard.add_button(label=buttons_titles[0], color=VkKeyboardColor.NEGATIVE)
            self.inline_keyboard.add_button(label=buttons_titles[1], color=VkKeyboardColor.POSITIVE)
        else:
            for button in buttons_titles:
                self.inline_keyboard.add_button(label=button, color=color)
        return self.inline_keyboard.get_keyboard()
