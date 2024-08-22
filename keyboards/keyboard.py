from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard:
    """
    Класс для создания клавиатур VK бота.
    """
    def __init__(self):
        """
        Инициализирует новый клавиатурный макет
        Аргументы:
            one_time (bool): Скрыть клавиатуру после взаимодействия пользователя с ней. Defaults to False.
            inline (bool): Inline клавиатура. Defaults to False.
        """
        self.keyboard = VkKeyboard()
        self.inline_keyboard = VkKeyboard(inline=True)
        self.settings_keyboard = VkKeyboard(inline=True)

    def get_keyboards(self, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=False):
        """
        Возвращает клавиатурный макет в виде словаря.
        Аргументы:
            buttons_titles (List[str]): Список заголовков кнопок для добавления в клавиатуру.
            color (VkKeyboardColor, optional): Цвет кнопок. Defaults to VkKeyboardColor.SECONDARY.
            one_time (bool, optional): Скрыть клавиатуру после взаимодействия пользователя с ней. Defaults to False.
        Возвращает:
            dict: Клавиатурный макет.
        """
        self.keyboard.one_time = one_time
        for button in buttons_titles:
            self.keyboard.add_button(label=button, color=color)
        return self.keyboard.get_keyboard()

    def get_inline_keyboards(self, found_user: dict, buttons_titles: list[str], color=VkKeyboardColor.SECONDARY, one_time=True):
        """
        Возвращает инлайн-клавиатурный макет в виде словаря.
        Аргументы:
            buttons_titles (List[str]): Список заголовков кнопок для добавления в инлайн-клавиатуру.
            color (VkKeyboardColor, optional): Цвет кнопок. Defaults to VkKeyboardColor.SECONDARY.
        Возвращает:
            dict: Инлайн-клавиатурный макет.
        """
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
        """
        Возвращает клавиатурный макет для настроек в виде словаря.
        Аргументы:
            buttons_titles (List[str]): Список заголовков кнопок для добавления в клавиатуру настроек.
            color (VkKeyboardColor, optional): Цвет кнопок. Defaults to VkKeyboardColor.SECONDARY.
            one_time (bool, optional): Скрыть после взаимодействия пользователя с ней. Defaults to False.
        Возвращает:
            dict: Клавиатурный макет для настроек.
        """
        settings_keyboard = VkKeyboard(inline=True)
        if len(buttons_titles) == len(actions):
            for i in range(len(buttons_titles)):
                settings_keyboard.add_button(label=buttons_titles[i], color=color,
                                                  payload={"action": actions[i], "user_id": user_id})
                if i == 1:
                    settings_keyboard.add_line()
        return settings_keyboard.get_keyboard()

    @staticmethod
    def get_new_search_keyboard(button_title: str, color=VkKeyboardColor.SECONDARY):
        """
        Возвращает клавиатурный макет для нового поиска в виде словаря.
        Аргументы:
            buttons_titles (List[str]): Список заголовков кнопок для добавления в клавиатуру новой поисковой строки.
            color (VkKeyboardColor, optional): Цвет кнопок. Defaults to VkKeyboardColor.SECONDARY.
            one_time (bool, optional): Скрыть после взаимодействия пользователя с ней. Defaults to False.
        Возвращает:
            dict: Клавиатурный макет для нового поиска.
        """
        keyboard = VkKeyboard(inline=True)
        keyboard.add_button(label=button_title, color=color)
        return keyboard.get_keyboard()
