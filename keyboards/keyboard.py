from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    def __init__(self):
        self.keyboard = VkKeyboard()
        self.inline_keyboard = VkKeyboard(inline=True)
        self.settings_keyboard = VkKeyboard(inline=True)

    def get_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        self.keyboard.one_time = one_time
        for button in buttons_titles:
            self.keyboard.add_button(label=button, color=color)
        return self.keyboard.get_keyboard()

    def get_inline_keyboards(self, found_user: dict, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=True):
        self.inline_keyboard.one_time = one_time
        if len(buttons_titles) == 2:
            self.inline_keyboard.add_button(label=buttons_titles[0], color=VkKeyboardColor.NEGATIVE,
                                            payload={"action": "add_to_blacklist", "user_id": found_user['id'],
                                                     "first_name": found_user['first_name'],
                                                     "last_name": found_user['last_name']})
            self.inline_keyboard.add_button(label=buttons_titles[1], color=VkKeyboardColor.POSITIVE,
                                            payload={"action": "add_to_favorite", "user_id": found_user['id'],
                                                     "first_name": found_user['first_name'],
                                                     "last_name": found_user['last_name']})
        else:
            for button in buttons_titles:
                self.inline_keyboard.add_button(label=button, color=color)
        return self.inline_keyboard.get_keyboard()

    @staticmethod
    def get_settings_keyboard(user_id: int, buttons_titles: list[str],
                              actions: list[str], color=VkKeyboardColor.PRIMARY):
        settings_keyboard = VkKeyboard(inline=True)
        if len(buttons_titles) == len(actions):
            for i in range(len(buttons_titles)):
                settings_keyboard.add_button(label=buttons_titles[i], color=color,
                                                  payload={"action": actions[i], "user_id": user_id})
                if i == 1:
                    settings_keyboard.add_line()
        return settings_keyboard.get_keyboard()
