import json
from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from database.db_vkbot import DBManager
from keyboards.keyboard import Keyboard
from models.vk_user import VKUser
from settings.config import settings
from source.vk_core import VKCore
from settings.messages import STICKS, MESSAGES


class VKBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=settings.token)
        self.vk = vk_api.VkApi(token=settings.api_token).get_api()
        self.DB = DBManager()
        self.longpoll = VkLongPoll(vk=self.vk_session, group_id=int(settings.group_id))
        self.start_keyboard = Keyboard().get_keyboards(['Начать', 'Инструкция'], one_time=True)
        self.working_keyboard = Keyboard().get_keyboards(['Меню', 'Избранное', 'Следующий'])
        self.vk_core = VKCore(settings.api_token)
        self.current_found_person_index = -1
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

    def send_keyboard(self, user_id, keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': 'Используйте клавиатуру',
                                                 'keyboard': keyboard, 'random_id': randrange(10 ** 7)})

    def send_inline_keyboard(self, user_id, inline_keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': 'Выберите действие:',
                                                 'keyboard': inline_keyboard, 'random_id': randrange(10 ** 7)})

    def send_stick(self, user_id, id_stick):
        self.vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                                 'random_id': randrange(10 ** 7), })

    def send_next_found_person(self, user_id: int, found_users: list[dict]):
        if self.current_found_person_index < len(found_users):
            self.current_found_person_index += 1
            current_found_user = found_users[self.current_found_person_index]
            all_users_photos = self.vk_core.get_all_users_photos(owner_id=current_found_user['id'])
            best_users_photos = self.vk_core.get_users_best_photos(all_users_photos)
            self.send_msg(user_id, f"{current_found_user['first_name']} {current_found_user['last_name']}\n "
                                   f"Профиль: https://vk.com/id{current_found_user['id']}")
            for user_photo in best_users_photos:
                self.send_photo_msg(user_id, user_photo['owner_id'], user_photo['id'])
            items_keyboard = Keyboard()
            items_keyboard = items_keyboard.get_inline_keyboards(
                current_found_user['id'],
                ['Добавить в черный список', 'Добавить в избранное'])
            self.send_inline_keyboard(user_id, items_keyboard)
        else:
            self.send_msg(user_id, "Список найденных пользователей закончился")

    def add_to_blacklist(self, banned_id: int, bot_user) -> None:
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_blacklist(blacklist_id=banned_id, vk_user=user)
        if adding_result:
            self.send_msg(bot_user.id, f"Пользователь {banned_id} добавлен в черный список")
        else:
            self.send_msg(bot_user.id, f"Пользователь {banned_id} уже в черном списке")

    def add_to_favourites(self, favourite_id: int, bot_user) -> None:
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_favourites(favourites_id=favourite_id, vk_user=user)
        if adding_result:
            self.send_msg(bot_user.id, f"Пользователь {favourite_id} добавлен в избранное")
        else:
            self.send_msg(bot_user.id, f"Пользователь {favourite_id} уже в избранном")

    def get_favourites(self, bot_user_id):
        users_data = self.DB.select_vk_users_data(bot_user_id)
        users_data = users_data[0]
        favourites = [favourite.id for favourite in users_data.favourites]
        favourites = ", ".join(map(str, favourites))
        return favourites

    def pressed_show_favourites(self, event):
        favourites = self.get_favourites(event.user_id)
        self.send_msg(event.user_id, f"Ваши избранные пользователи: {favourites}")
        self.send_keyboard(event.user_id, self.working_keyboard)

    def pressed_show_menu(self, event):
        self.send_msg(event.user_id, f"Вы вошли в меню")
        self.send_keyboard(event.user_id, self.working_keyboard)

    def pressed_start(self, event):
        self.current_found_person_index = -1
        self.vk_core.get_profiles_info(event.user_id)
        vk_user = self.vk_core.vk_bot_user
        self.current_user = self.DB.select_vk_user(event.user_id)
        if not self.current_user:
            self.current_user = VKUser(id=event.user_id, first_name=vk_user.first_name)
            self.DB.insert_vk_user(self.current_user)
        self.send_msg(event.user_id, "Идет поиск. Подождите...")
        search_res = self.vk_core.search_users(age=vk_user.age, city=vk_user.city_id, sex=vk_user.sex)
        self.found_users = search_res.get('items')
        self.send_msg(event.user_id, f"Поиск завершен. "
                                     f"Для вас найдено {len(self.found_users)} пользователей:")
        self.send_keyboard(event.user_id, self.working_keyboard)
        self.send_next_found_person(event.user_id, self.found_users)

    def start_pooling(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text.strip().lower()
                    print(request)
                    if request == "привет" or request == "hello":
                        self.send_msg(event.user_id, f"Привет, {event.user_id}")
                        self.send_stick(event.user_id, STICKS['HELLO'])
                        self.send_keyboard(event.user_id, self.start_keyboard)
                    elif request == "начать" or request == "start":
                        self.pressed_start(event)
                        if self.found_users:
                            self.send_next_found_person(event.user_id, self.found_users)
                    elif request == "следующий" or request == "next":
                        if self.found_users:
                            self.send_next_found_person(event.user_id, self.found_users)
                        else:
                            self.send_msg(event.user_id, "По вашему запросу ничего не найдено")
                            self.send_msg(event.user_id, "Начните поиск заново")
                            self.send_keyboard(event.user_id, self.start_keyboard)
                    elif request == "инструкция" or request == "help":
                        self.send_stick(event.user_id, STICKS['HELP'])
                        self.send_msg(event.user_id, MESSAGES['HELP'])
                    elif request == "пока" or request == "goodbye":
                        self.send_msg(event.user_id, "Уже выходите?...Пока((")
                        self.send_stick(event.user_id, STICKS['GOODBYE'])
                    elif request == "избранное" or request == "favourites":
                        self.pressed_show_favourites(event)
                    elif request == "меню" or request == "menu":
                        self.pressed_show_menu(event)
                    elif request == "добавить в избранное":
                        payload = json.loads(event.extra_values.get('payload'))
                        if payload:
                            self.add_to_favourites(payload.get('user_id'), self.current_user)
                    elif request == "добавить в черный список":
                        payload = json.loads(event.extra_values.get('payload'))
                        if payload:
                            self.add_to_blacklist(payload.get('user_id'), self.current_user)
                    else:
                        self.send_msg(event.user_id, "Не понял вашего ответа...")
                        self.send_stick(event.user_id, STICKS['MISUNDERSTAND'])
