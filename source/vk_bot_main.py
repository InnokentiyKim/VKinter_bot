import json
from source.vk_bot_core import CoreVkLongPoll
from vk_api.longpoll import VkEventType
from settings.config import settings, COMMANDS
from source.vk_bot_func import VKBotFunc
from settings.messages import STICKS, MESSAGES


class VKBot:
    """
    Главный класс для бота VKinter.
    Реализует работу и управление ботом.
    """
    def __init__(self):
        """
        Атрибуты:
            bot_func (source.vk_bot_func.VKBotFunc): Объект для работы с функциями бота.
            longpoll (CoreVkLongPoll): Объект для работы с лонгпуллом.
        """
        self.bot_func = VKBotFunc()
        self.longpoll = CoreVkLongPoll(vk=self.bot_func.vk_session, group_id=int(settings.group_id))

    def pressed_hello(self, event):
        """
        Обрабатывает нажатие на команду "Привет".
        """
        self.bot_func.send_msg(event.user_id, f"{MESSAGES['HELLO']}, {event.user_id}")
        self.bot_func.send_stick(event.user_id, STICKS['HELLO'])
        self.bot_func.send_keyboard(event.user_id, self.bot_func.start_keyboard)

    def pressed_bye(self, event):
        """
        Обрабатывает нажатие на команду "Пока".
        """
        self.bot_func.send_msg(event.user_id, MESSAGES['GOODBYE'])
        self.bot_func.send_stick(event.user_id, STICKS['GOODBYE'])

    def pressed_help(self, event):
        """
        Обрабатывает нажатие на команду "Помощь".
        """
        self.bot_func.send_stick(event.user_id, STICKS['HELP'])
        self.bot_func.send_msg(event.user_id, MESSAGES['HELP'])

    def pressed_start(self, event):
        """
        Обрабатывает нажатие на команду "Начать".
        """
        self.bot_func.starting_actions(event.user_id)

    def pressed_new_search(self, event):
        """
        Обрабатывает нажатие на команду "Начать новый поиск".
        """
        self.bot_func.starting_actions(event.user_id, use_new_settings=True)

    def pressed_next(self, event):
        """
        Обрабатывает нажатие на команду "Следующий".
        """
        if self.bot_func.found_users:
            self.bot_func.send_next_found_person(event.user_id, self.bot_func.found_users)
        else:
            self.pressed_start(event)

    def pressed_to_blacklist(self, event) -> None:
        """
        Обрабатывает нажатие на команду "В черный список".
        """
        payload = json.loads(event.extra_values.get('payload'))
        if payload:
            self.bot_func.add_to_blacklist(payload, self.bot_func.current_user)
        else:
            self.bot_func.send_msg(event.user_id, MESSAGES['UNKNOWN_ID'])

    def pressed_to_favourites(self, event) -> None:
        """
        Обрабатывает нажатие на команду "В избранное".
        """
        payload = json.loads(event.extra_values.get('payload'))
        if payload:
            self.bot_func.add_to_favourites(payload, self.bot_func.current_user)
        else:
            self.bot_func.send_msg(event.user_id, MESSAGES['UNKNOWN_ID'])

    def pressed_show_favourites(self, event):
        """
        Обрабатывает нажатие на команду "Избранное".
        """
        self.bot_func.get_favourites(event.user_id)

    def pressed_settings(self, event):
        """
        Обрабатывает нажатие на команду "Настройки".
        """
        self.bot_func.get_settings(event.user_id)

    def pressed_about(self, event):
        """
        Обрабатывает нажатие на команду "О боте".
        """
        self.bot_func.send_msg(event.user_id, MESSAGES['ABOUT'])

    def pressed_settings_increase_age(self, event):
        """
        Обрабатывает нажатие на команду "Увеличить возраст поиска".
        """
        self.bot_func.settings_increase_age(event.user_id)

    def pressed_settings_decrease_age(self, event):
        """
        Обрабатывает нажатие на команду "Уменьшить возраст поиска".
        """
        self.bot_func.settings_decrease_age(event.user_id)

    def pressed_settings_ignore_blacklist(self, event):
        """
        Обрабатывает нажатие на команду "Игнорировать черный список".
        """
        self.bot_func.settings_ignore_blacklist(event.user_id)

    def pressed_settings_reset(self, event):
        """
        Обрабатывает нажатие на команду "Сбросить настройки".
        """
        self.bot_func.settings_reset(event.user_id)

    def unknown_command(self, event):
        """
        Обрабатывает неизвестную команду.
        """
        self.bot_func.send_msg(event.user_id, MESSAGES['MISUNDERSTAND'])
        self.bot_func.send_stick(event.user_id, STICKS['MISUNDERSTAND'])

    def start_pooling(self):
        """
        Запускает бесконечный цикл обработки событий.
        Обрабатывает каждое событие, полученное от ВКонтакте.
        """
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text.strip().lower()
                if request == COMMANDS['HELLO']:
                    self.pressed_hello(event)
                elif request == COMMANDS['START']:
                    self.pressed_start(event)
                elif request == COMMANDS['NEXT']:
                    self.pressed_next(event)
                elif request == COMMANDS['HELP']:
                    self.pressed_help(event)
                elif request == COMMANDS['GOODBYE']:
                    self.pressed_bye(event)
                elif request == COMMANDS['SHOW_FAVOURITES']:
                    self.pressed_show_favourites(event)
                elif request == COMMANDS['CONFIG']:
                    self.pressed_settings(event)
                elif request == COMMANDS['TO_FAVOURITES']:
                    self.pressed_to_favourites(event)
                elif request == COMMANDS['TO_BLACKLIST']:
                    self.pressed_to_blacklist(event)
                elif request == COMMANDS['TO_BLACKLIST']:
                    self.pressed_to_blacklist(event)
                elif request == COMMANDS['ABOUT']:
                    self.pressed_about(event)
                elif request == COMMANDS['INCREASE_AGE']:
                    self.pressed_settings_increase_age(event)
                elif request == COMMANDS['DECREASE_AGE']:
                    self.pressed_settings_decrease_age(event)
                elif request == COMMANDS['IGNORE_BLACKLIST']:
                    self.pressed_settings_ignore_blacklist(event)
                elif request == COMMANDS['RESET_SETTINGS']:
                    self.pressed_settings_reset(event)
                elif request == COMMANDS['NEW_SEARCH']:
                    self.pressed_new_search(event)
                else:
                    self.unknown_command(event)
