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
        self.start_keyboard = Keyboard().get_keyboards(['Начать', 'Инструкция'])

    def send_chat_msg(self, chat_id, message):
        self.vk_session.method('messages.send', {'chat_id': chat_id, 'message': message,
                                                 'random_id': randrange(10 ** 7), })

    def send_msg(self, user_id, message):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                 'random_id': randrange(10 ** 7), })

    def send_keyboard(self, user_id, keyboard):
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': 'Клавиатура',
                                                 'keyboard': keyboard, 'random_id': randrange(10 ** 7)})

    def send_stick(self, user_id, id_stick):
        self.vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                                 'random_id': randrange(10 ** 7), })

    def start_pooling(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    request = event.text.strip().lower()
                    if request == "привет":
                        self.send_msg(event.user_id, f"Привет, {event.user_id}")
                        self.send_stick(event.user_id, STICKS['HELLO'])
                    elif request == "start":
                        self.send_keyboard(event.user_id, self.start_keyboard)
                        self.send_stick(event.user_id, STICKS['START'])
                    elif request == "help":
                        self.send_msg(event.user_id, f"Помощь")
                        self.send_stick(event.user_id, STICKS['HELP'])
                    elif request == "пока":
                        self.send_msg(event.user_id, "Пока((")
                        self.send_stick(event.user_id, STICKS['GOODBYE'])
                    else:
                        # vk_user = VKCore(settings.api_token)
                        # vk_user.get_profiles_info(event.user_id)
                        # print(f"{vk_user.first_name=} {vk_user.last_name=} {vk_user.age=} {vk_user.city=}"
                        #       f"{vk_user.relation} {vk_user.phone=} {vk_user.sex} {vk_user.photo=}")
                        self.send_msg(event.user_id, "Не понял вашего ответа...")
                        self.send_stick(event.user_id, STICKS['MISUNDERSTAND'])
