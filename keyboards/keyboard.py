from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self):
        self.keyboard = VkKeyboard()
        self.inline_keyboard = VkKeyboard(inline=True)

    def get_keyboard(self, title: str, color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        self.keyboard.add_button(label=title, color=color)
        return self.keyboard.get_keyboard()

    def get_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        for button in buttons_titles:
            self.keyboard.add_button(label=button, color=color)
        return self.keyboard.get_keyboard()

    def get_inline_keyboards(self, user_id: int, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=True):
        self.inline_keyboard.one_time = one_time
        if len(buttons_titles) == 2:
            self.inline_keyboard.add_button(label=buttons_titles[0], color=VkKeyboardColor.NEGATIVE,
                                            payload={"action": "add_to_blacklist", "user_id": user_id})
            self.inline_keyboard.add_button(label=buttons_titles[1], color=VkKeyboardColor.POSITIVE,
                                            payload={"action": "add_to_favorite", "user_id": user_id})
        else:
            for button in buttons_titles:
                self.inline_keyboard.add_button(label=button, color=color)
        return self.inline_keyboard.get_keyboard()
