from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from settings.config import settings
from source.vk_core import VKUser


vk_session = vk_api.VkApi(token=settings.token)
vk = vk_api.VkApi(token=settings.api_token).get_api()
start_keyboard = VkKeyboard()
start_keyboard.add_button('Начать', color=VkKeyboardColor.SECONDARY)
start_keyboard.add_button('Инструкция', color=VkKeyboardColor.SECONDARY)
longpoll = VkLongPoll(vk=vk_session, group_id=int(settings.group_id))


def send_chat_msg(chat_id, message):
    vk_session.method('messages.send', {'chat_id': chat_id, 'message': message,
                                        'random_id': randrange(10 ** 7), })


def send_msg(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                        'random_id': randrange(10 ** 7), })


def send_keyboard(user_id, keyboard):
    vk_session.method('messages.send', {'user_id': user_id, 'message': 'Клавиатура',
                                        'keyboard': keyboard.get_keyboard(), 'random_id': randrange(10 ** 7), })


def send_stick(user_id, id_stick):
    vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                        'random_id': randrange(10 ** 7), })


def vk_bot():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.strip().lower()
                if request == "привет":
                    send_msg(event.user_id, f"Привет, {event.from_user['first_name']}")
                    send_stick(event.user_id, 112)
                elif request == "start":
                    send_keyboard(event.user_id, start_keyboard)
                elif request == "пока":
                    send_msg(event.user_id, "Пока((")
                else:
                    vk_user = VKUser(settings.api_token)
                    vk_user.get_profiles_info(event.user_id)
                    users_info = vk.account.getProfileInfo(user_id=event.user_id)
                    print(f"{vk_user.first_name=} {vk_user.last_name=} {vk_user.age=} {vk_user.city=}"
                          f"{vk_user.relation} {vk_user.phone=} {vk_user.sex} {vk_user.photo=}")
                    send_msg(event.user_id, "Не поняла вашего ответа...")


def main():
    print("Бот запущен...")
    vk_bot()


if __name__ == '__main__':
    main()
