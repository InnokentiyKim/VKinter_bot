from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from keyboards.keyboard import Keyboard
from settings.config import settings
from source.vk_core import VKCore
from settings.messages import STICKS


class VKBot:
    def __init__(self):
        self.vk_session = vk_api.VkApi(token=settings.token)
        self.vk = vk_api.VkApi(token=settings.api_token).get_api()
        self.longpoll = VkLongPoll(vk=self.vk_session, group_id=int(settings.group_id))
        self.start_keyboard = Keyboard().get_keyboards(['Начать', 'Инструкция'], one_time=True)
        self.working_keyboard = Keyboard().get_keyboards(['Предыдущий', 'Следующий'])
        self.vk_core = VKCore(settings.api_token)
        self.current_found_person_index = -1
        self.found_users = []

    def send_chat_msg(self, chat_id, message):
        self.vk_session.method('messages.send', {'chat_id': chat_id, 'message': message,
                                                 'random_id': randrange(10 ** 7), })

    def send_msg(self, user_id: int, message: str, send_photo: bool = False, photo_attach: list[str] = None):
        if not send_photo:
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'random_id': randrange(10 ** 7), })
        else:
            attachment = f"photo-{photo_attach[0]}_{photo_attach[1]}" if photo_attach else ""
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'attachment': attachment, 'random_id': randrange(10 ** 7), })

    def send_keyboard(self, user_id, keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': 'Используйте клавиатуру',
                                                 'keyboard': keyboard, 'random_id': randrange(10 ** 7)})

    def send_stick(self, user_id, id_stick):
        self.vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                                 'random_id': randrange(10 ** 7), })

    def send_next_found_person(self, user_id: int, found_users: list[dict]):
        if self.current_found_person_index < len(found_users):
            self.current_found_person_index += 1
            current_user = found_users[self.current_found_person_index]
            users_photos = self.vk_core.get_users_photos(owner_id=current_user['id'])
            print(users_photos)
            self.send_msg(user_id,
                          f"{current_user['first_name']} {current_user['last_name']}\n "
                          f"Профиль: https://vk.com/id{current_user['id']}",
                          send_photo=True, photo_attach=[current_user['id'], current_user['photo_400_orig']])

    def start_pooling(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text.strip().lower()
                    if request == "привет" or request == "hello":
                        self.send_msg(event.user_id, f"Привет, {event.user_id}")
                        self.send_stick(event.user_id, STICKS['HELLO'])
                        self.send_keyboard(event.user_id, self.start_keyboard)
                    elif request == "начать" or request == "start":
                        self.vk_core.get_profiles_info(event.user_id)
                        vk_user = self.vk_core.vk_bot_user
                        search_res = self.vk_core.search_users(age=vk_user.age, city=vk_user.city_id)
                        self.found_users = search_res.get('items')
                        self.send_keyboard(event.user_id, self.working_keyboard)
                    elif request == "следующий" or request == "next":
                        if self.found_users:
                            self.send_next_found_person(event.user_id, self.found_users)
                        else:
                            self.send_msg(event.user_id, "По вашему запросу ничего не найдено")
                            self.send_msg(event.user_id, "Начните поиск заново")
                            self.send_keyboard(event.user_id, self.start_keyboard)
                    elif request == "инструкция" or request == "help":
                        self.send_msg(event.user_id, f"Помощь")
                        self.send_stick(event.user_id, STICKS['HELP'])
                    elif request == "пока" or request == "goodbye":
                        self.send_msg(event.user_id, "Пока((")
                        self.send_stick(event.user_id, STICKS['GOODBYE'])
                    else:
                        self.send_msg(event.user_id, "Не понял вашего ответа...")
                        self.send_stick(event.user_id, STICKS['MISUNDERSTAND'])
