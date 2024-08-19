import json
from source.vk_bot_core import CoreVkLongPoll
from vk_api.longpoll import VkEventType
from settings.config import settings, COMMANDS
from source.vk_bot_func import VKBotFunc
from settings.messages import STICKS, MESSAGES


class VKBot:
    def __init__(self):
        self.bot_func = VKBotFunc()
        self.longpoll = CoreVkLongPoll(vk=self.bot_func.vk_session, group_id=int(settings.group_id))

    def pressed_hello(self, event):
        self.bot_func.send_msg(event.user_id, f"Привет, {event.user_id}")
        self.bot_func.send_stick(event.user_id, STICKS['HELLO'])
        self.bot_func.send_keyboard(event.user_id, self.bot_func.start_keyboard)

    def pressed_bye(self, event):
        self.bot_func.send_msg(event.user_id, "Уже выходите?...Пока((")
        self.bot_func.send_stick(event.user_id, STICKS['GOODBYE'])

    def pressed_help(self, event):
        self.bot_func.send_stick(event.user_id, STICKS['HELP'])
        self.bot_func.send_msg(event.user_id, MESSAGES['HELP'])

    def pressed_start(self, event):
        self.bot_func.starting_actions(event.user_id)

    def pressed_new_search(self, event):
        self.bot_func.starting_actions(event.user_id, use_new_settings=True)

    def pressed_next(self, event):
        if self.bot_func.found_users:
            self.bot_func.send_next_found_person(event.user_id, self.bot_func.found_users)
        else:
            self.pressed_start(event)

    def pressed_to_blacklist(self, event) -> None:
        payload = json.loads(event.extra_values.get('payload'))
        if payload:
            self.bot_func.add_to_blacklist(payload, self.bot_func.current_user)
        else:
            self.bot_func.send_msg(event.user_id, "Не удалось определить id пользователя...")

    def pressed_to_favourites(self, event) -> None:
        payload = json.loads(event.extra_values.get('payload'))
        if payload:
            self.bot_func.add_to_favourites(payload, self.bot_func.current_user)
        else:
            self.bot_func.send_msg(event.user_id, "Не удалось определить id пользователя...")

    def pressed_show_favourites(self, event):
        self.bot_func.get_favourites(event.user_id)

    def pressed_settings(self, event):
        self.bot_func.get_settings(event.user_id)

    def pressed_about(self, event):
        self.bot_func.send_msg(event.user_id, MESSAGES['ABOUT'])

    def pressed_settings_increase_age(self, event):
        self.bot_func.settings_increase_age(event.user_id)

    def pressed_settings_decrease_age(self, event):
        self.bot_func.settings_decrease_age(event.user_id)

    def pressed_settings_ignore_blacklist(self, event):
        self.bot_func.settings_ignore_blacklist(event.user_id)

    def pressed_settings_reset(self, event):
        self.bot_func.settings_reset(event.user_id)

    def unknown_command(self, event):
        self.bot_func.send_msg(event.user_id, "Не понял вашего ответа...")
        self.bot_func.send_stick(event.user_id, STICKS['MISUNDERSTAND'])

    def start_pooling(self):
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
