from random import randrange
import vk_api
from database.db_vkbot import DBManager
from keyboards.keyboard import Keyboard
from models.vk_user import VKUser
from settings.config import settings, STATUS, COMMANDS
from source.vk_bot_core import BotSettings
from source.vk_core import VKCore


class VKBotFunc:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=settings.token)
        self.vk = vk_api.VkApi(token=settings.api_token).get_api()
        self.DB = DBManager()
        self.start_keyboard = Keyboard().get_keyboards(['Начать', 'Инструкция'], one_time=True)
        self.working_keyboard = Keyboard().get_keyboards(['Настройки', 'Избранное', 'Следующий'])
        self.vk_core = VKCore(settings.api_token)
        self.bot_settings = BotSettings()
        self.found_person_index = -1
        self.current_user = None
        self.found_users = []

    def send_chat_msg(self, chat_id, message):
        self.vk_session.method('messages.send', {'chat_id': chat_id, 'message': message,
                                                 'random_id': randrange(10 ** 7), })

    def send_msg(self, user_id: int, message: str, send_photo: bool = False, photo_attach: list[str] = None):
        if not send_photo:
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'random_id': randrange(10 ** 7), })
        else:
            attachment = f"photo {photo_attach[0]}_{photo_attach[1]}" if photo_attach else ""
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'attachment': attachment, 'random_id': randrange(10 ** 7), })

    def send_photo_msg(self, user_id: int, owner_id: str, photo_id: str, message: str = None):
        attachment = f"photo{owner_id}_{photo_id}"
        if message:
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'attachment': attachment, 'random_id': randrange(10 ** 7), })
        else:
            self.vk_session.method('messages.send', {'user_id': user_id, 'attachment': attachment,
                                                     'random_id': randrange(10 ** 7), })

    def send_keyboard(self, user_id, keyboard, message: str = 'Используйте клавиатуру:'):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                 'keyboard': keyboard, 'random_id': randrange(10 ** 7)})

    def send_inline_keyboard(self, user_id, inline_keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': 'Выберите действие:',
                                                 'keyboard': inline_keyboard, 'random_id': randrange(10 ** 7)})

    def send_stick(self, user_id, id_stick):
        self.vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                                 'random_id': randrange(10 ** 7), })

    def _find_next_suitable_profile(self, found_users: list[dict]) -> dict | None:
        while self.found_person_index < len(found_users):
            self.found_person_index += 1
            found_user = found_users[self.found_person_index]
            if not found_user['is_closed']:
                if self.current_user and self.bot_settings.use_blacklist:
                    if self.current_user.blacklist:
                        blacklist_ids = [blacklist.id for blacklist in self.current_user.blacklist]
                        if found_user['id'] in blacklist_ids:
                            continue
                    if 'relation' in found_user:
                        if found_user['relation'] not in STATUS.values():
                            continue
                    return found_user
                else:
                    if 'relation' in found_user:
                        if found_user['relation'] not in STATUS.keys():
                            continue
                    return found_user
        return None

    def _form_user_card(self, user_id: int, found_user: dict) -> None:
        users_photos = self.vk_core.get_users_photos(owner_id=found_user['id'])
        self.send_msg(user_id, f"{found_user['first_name']} {found_user['last_name']}\n "
                               f"Профиль: https://vk.com/id{found_user['id']}")
        for photo in users_photos:
            self.send_photo_msg(user_id, photo['owner_id'], photo['id'])
        items_keyboard = Keyboard().get_inline_keyboards(
            found_user, ['Добавить в черный список', 'Добавить в избранное'])
        self.send_inline_keyboard(user_id, items_keyboard)

    def send_next_found_person(self, user_id: int, found_users: list[dict]):
        found_user = self._find_next_suitable_profile(found_users)
        print(found_user)
        if found_user:
            self._form_user_card(user_id, found_user)
        else:
            self.send_msg(user_id, "Список найденных пользователей закончился")

    def add_to_blacklist(self, payload: dict, bot_user) -> None:
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_blacklist(banned=payload, vk_user=user)
        if adding_result:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} добавлен(-а) в черный список")
        elif adding_result is False:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} уже в черном списке")
        else:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} не найден")

    def add_to_favourites(self, payload: dict, bot_user) -> None:
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_favourites(favourites=payload, vk_user=user)
        if adding_result is True:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} добавлен(-а) в избранное")
        elif adding_result is False:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} уже в избранном")
        else:
            self.send_msg(bot_user.id, f"Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} не найден")

    def get_favourites(self, bot_user_id: int) -> None:
        users_data = self.DB.select_vk_users_data(bot_user_id)
        favourites_list = users_data.favourites
        if favourites_list:
            favourites_list_msg = ""
            for favourite in favourites_list:
                profile = f"[https://vk.com/id{favourite.id}]"
                favourites_list_msg += f"{favourite.first_name} {favourite.last_name} {profile}\n"
            self.send_msg(bot_user_id, f"Ваши избранные пользователи:\n {favourites_list_msg}")
        else:
            self.send_msg(bot_user_id, f"Список избранных пользователей пуст")

    def get_settings(self, user_id: int) -> None:
        settings_keyboard = Keyboard().get_settings_keyboard(
            user_id=user_id,
            buttons_titles=[
                COMMANDS['DECREASE_AGE'],
                COMMANDS['INCREASE_AGE'],
                COMMANDS['IGNORE_BLACKLIST'],
                COMMANDS['RESET_SETTINGS']
                ],
            actions=[
                'age_down',
                'age_up',
                'blacklist_off',
                'reset_settings']
        )
        self.send_keyboard(user_id, settings_keyboard, 'Настройки поиска')

    def starting_actions(self, user_id: int) -> None:
        self.found_person_index = -1
        self.vk_core.get_profiles_info(user_id)
        vk_user = self.vk_core.vk_bot_user
        self.current_user = self.DB.select_vk_users_data(user_id)
        if not self.current_user:
            self.current_user = VKUser(id=user_id, first_name=vk_user.first_name, last_name=vk_user.last_name)
            self.DB.insert_vk_user(self.current_user)
            self.current_user = self.DB.select_vk_users_data(user_id)
        self.send_msg(user_id, "Идет поиск. Подождите...")
        self.bot_settings.reset_settings(vk_user.age)
        search_res = self.vk_core.search_users(age_from=self.bot_settings.age_from, age_to=self.bot_settings.age_to,
                                               city=vk_user.city_id, sex=vk_user.sex)
        self.found_users = search_res.get('items')
        self.send_keyboard(user_id, self.working_keyboard)
        self.send_next_found_person(user_id, self.found_users)
