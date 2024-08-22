from random import randrange
import vk_api
from database.db_vkbot import DBManager
from keyboards.keyboard import Keyboard
from models.vk_user import VKUser
from settings.config import settings, STATUS, COMMANDS
from settings.messages import MESSAGES
from source.vk_bot_core import BotSettings
from source.vk_core import VKCore
from bot_logging.bot_logging import bot_exception_logger, LOGGER_PATH


class VKBotFunc:
    """
    Класс, реализующий основной функционал бота.
    """
    def __init__(self):
        """
        Атрибуты:
            vk_session (vk_api.VkApi): Объект сессии VK API.
            vk (vk_api.VkApiMethod): Объект методов VK API.
            DB (database.db_vkbot.DBManager): Объект для работы с базой данных.
            start_keyboard (list[list[str]]): Начальная клавиатура.
            working_keyboard (list[list[str]]): Клавиатура для работы с ботом.
            new_search_keyboard (list[list[str]]): Клавиатура для начала нового поиска.
            vk_core (source.vk_bot_core.VKCore): Основной объект для работы с VK API.
            bot_settings (source.vk_bot_core.BotSettings): Объект для работы с настройками бота.
            found_person_index (int): Индекс пользователя в списке найденных пользователей.
            current_user (VKUser): Текущий пользователь.
            found_users (list[VKUser]): Список найденных пользователей.
        """
        self.vk_session = vk_api.VkApi(token=settings.token)
        self.vk = vk_api.VkApi(token=settings.api_token).get_api()
        self.DB = DBManager()
        self.start_keyboard = Keyboard().get_keyboards(['Начать', 'Инструкция'], one_time=True)
        self.working_keyboard = Keyboard().get_keyboards(['Настройки', 'Избранное', 'Следующий'])
        self.new_search_keyboard = Keyboard().get_new_search_keyboard('Начать новый поиск')
        self.vk_core = VKCore(settings.api_token)
        self.bot_settings = BotSettings()
        self.found_person_index = -1
        self.current_user = None
        self.found_users = []

    def send_chat_msg(self, chat_id, message):
        """
        Отправляет сообщение в чат.
        Параметры:
            chat_id (int): ID чата.
            message (str): Текст сообщения.
        """
        self.vk_session.method('messages.send', {'chat_id': chat_id, 'message': message,
                                                 'random_id': randrange(10 ** 7), })

    def send_msg(self, user_id: int, message: str, send_photo: bool = False, photo_attach: list[str] = None):
        """
        Отправляет сообщение пользователю чат-бота.
        Параметры:
            user_id (int): ID пользователя.
            message (str): Текст сообщения.
            send_photo (bool): Отправлять ли фото.
            photo_attach (list[str]): Список ID фото.
        """
        if not send_photo:
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'random_id': randrange(10 ** 7), })
        else:
            attachment = f"photo {photo_attach[0]}_{photo_attach[1]}" if photo_attach else ""
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'attachment': attachment, 'random_id': randrange(10 ** 7), })

    def send_photo_msg(self, user_id: int, owner_id: str, photo_id: str, message: str = None):
        """
        Отправляет фото пользователю чат-бота.
        Параметры:
            user_id (int): ID пользователя.
            owner_id (str): ID владельца фото.
            photo_id (str): ID фото.
            message (str): Текст сообщения.
        """
        attachment = f"photo{owner_id}_{photo_id}"
        if message:
            self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                     'attachment': attachment, 'random_id': randrange(10 ** 7), })
        else:
            self.vk_session.method('messages.send', {'user_id': user_id, 'attachment': attachment,
                                                     'random_id': randrange(10 ** 7), })

    def send_keyboard(self, user_id, keyboard, message: str = 'Используйте клавиатуру:'):
        """
        Отправляет сообщение пользователю чат-бота с клавиатурой.
        Параметры:
            user_id (int): ID пользователя.
            keyboard (list[list[str]]): Клавиатура.
            message (str): Текст сообщения.
        """
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                 'keyboard': keyboard, 'random_id': randrange(10 ** 7)})

    def send_inline_keyboard(self, user_id, inline_keyboard, message: str = 'Выберите действие:'):
        """
        Отправляет сообщение пользователю чат-бота с inline клавиатурой.
        Параметры:
            user_id (int): ID пользователя.
            inline_keyboard (list[list[str]]): Клавиатура.
            message (str): Текст сообщения.
        """
        self.vk_session.method('messages.send', {'user_id': user_id, 'message': message,
                                                 'keyboard': inline_keyboard, 'random_id': randrange(10 ** 7)})

    def send_stick(self, user_id, id_stick):
        """
        Отправляет стикер пользователю чат-бота.
        Параметры:
            user_id (int): ID пользователя.
            id_stick (int): ID стикера.
        """
        self.vk_session.method('messages.send', {'user_id': user_id, 'sticker_id': id_stick,
                                                 'random_id': randrange(10 ** 7), })

    @bot_exception_logger(LOGGER_PATH, exc_info=True)
    def _find_next_suitable_profile(self, found_users: list[dict]) -> dict | None:
        """
        Находит подходящего пользователя.
        Если подходящего пользователя нет, то возвращает None.
        Проверяет наличие в черном списке, статус пользователя и открытость профиля.
        Параметры:
            found_users (list[dict]): Список найденных пользователей.
        Возвращает:
            dict: Подходящего пользователя.
        """
        while self.found_person_index < len(found_users):
            self.found_person_index += 1
            found_user = found_users[self.found_person_index]
            if 'relation' in found_user:
                if found_user['relation'] not in STATUS.values():
                    continue
            if not found_user['is_closed']:
                if self.current_user and self.bot_settings.use_blacklist:
                    if self.current_user.blacklist:
                        blacklist_ids = [blacklist.id for blacklist in self.current_user.blacklist]
                        if found_user['id'] in blacklist_ids:
                            continue
                    return found_user
                else:
                    return found_user
        return None

    def _form_user_card(self, user_id: int, found_user: dict) -> None:
        """
        Формирует карточку пользователя.
        Параметры:
            user_id (int): ID пользователя.
            found_user (dict): Найденный пользователь.
        Возвращает: None
        """
        users_photos = self.vk_core.get_users_photos(owner_id=found_user['id'])
        self.send_msg(user_id, f"{found_user['first_name']} {found_user['last_name']}\n "
                               f"Профиль: https://vk.com/id{found_user['id']}")
        for photo in users_photos:
            self.send_photo_msg(user_id, photo['owner_id'], photo['id'])
        items_keyboard = Keyboard().get_inline_keyboards(
            found_user, ['Добавить в черный список', 'Добавить в избранное'])
        self.send_inline_keyboard(user_id, items_keyboard)

    def send_next_found_person(self, user_id: int, found_users: list[dict]):
        """
        Отправляет следующего подходящего пользователя.
        Если подходящего пользователя нет, то отправляет сообщение об окончании поиска.
        Параметры:
            user_id (int): ID пользователя.
            found_users (list[dict]): Список найденных пользователей.
        Возвращает: None
        """
        found_user = self._find_next_suitable_profile(found_users)
        if found_user:
            self._form_user_card(user_id, found_user)
        else:
            self.send_msg(user_id, MESSAGES['END_OF_LIST'])

    def add_to_blacklist(self, payload: dict, bot_user) -> None:
        """
        Добавляет пользователя в черный список.
        Если пользователь уже в черном списке или не найден, то отправляет сообщение об ошибке.
        Параметры:
            payload (dict): Полезная нагрузка (идентификация действия и пользователя).
            bot_user (VKUser): Пользователь чат-бота.
        """
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_blacklist(banned=payload, vk_user=user)
        if adding_result:
            self.send_msg(bot_user.id, f"🖤 Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} добавлен(-а) в черный список")
        elif adding_result is False:
            self.send_msg(bot_user.id, f"🖤 Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} уже в черном списке")
        else:
            self.send_msg(bot_user.id, f"🖤 Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} не найден")

    def add_to_favourites(self, payload: dict, bot_user) -> None:
        """
        Добавляет пользователя в избранное.
        Если пользователь уже в избранном или не найден, то отправляет сообщение об ошибке.
        Параметры:
            payload (dict): Полезная нагрузка (идентификация действия и пользователя).
            bot_user (VKUser): Пользователь чат-бота.
        """
        user = self.DB.select_vk_user(bot_user.id)
        adding_result = self.DB.insert_favourites(favourites=payload, vk_user=user)
        if adding_result is True:
            self.send_msg(bot_user.id, f"⭐ Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} добавлен(-а) в избранное 💓")
        elif adding_result is False:
            self.send_msg(bot_user.id, f"⭐ Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} уже в избранном 💓")
        else:
            self.send_msg(bot_user.id, f"⭐ Пользователь {(payload['user_id'])} "
                                       f"{payload['first_name']} {payload['last_name']} не найден")

    def get_favourites(self, bot_user_id: int) -> None:
        """
        Отправляет список избранных пользователей.
        Если список пуст, то отправляет сообщение об ошибке.
        Параметры:
            bot_user_id (int): ID пользователя чат-бота.
        Возвращает: None
        """
        users_data = self.DB.select_vk_users_data(bot_user_id)
        favourites_list = users_data.favourites
        if favourites_list:
            favourites_list_msg = ""
            for favourite in favourites_list:
                profile = f"[https://vk.com/id{favourite.id}]"
                favourites_list_msg += f"⭐ {favourite.first_name} {favourite.last_name} {profile}\n"
            self.send_msg(bot_user_id, f"💕 ⭐ Ваши избранные пользователи ⭐ 💕\n {favourites_list_msg}")
        else:
            self.send_msg(bot_user_id, f"⭐ Список избранных пользователей пуст 🚫")

    def get_settings(self, user_id: int) -> None:
        """
        Отправляет клавиатуру с настройками.
        Параметры:
            user_id (int): ID пользователя чат-бота.
        Возвращает: None
        """
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
        self.send_keyboard(user_id, settings_keyboard, MESSAGES['SETTINGS'])

    def starting_actions(self, user_id: int, use_new_settings: bool = False) -> None:
        """
        Выполняет начальные действия.
        Если пользователь не найден в базе данных, то добавляет его.
        Выполняет поиск новых пользователей и отправляет первого подходящего кандидата в чат.
        Параметры:
            user_id (int): ID пользователя чат-бота.
            use_new_settings (bool): Использовать ли новые настройки.
        Возвращает: None
        """
        self.found_person_index = -1
        self.vk_core.get_profiles_info(user_id)
        vk_user = self.vk_core.vk_bot_user
        self.current_user = self.DB.select_vk_users_data(user_id)
        if not self.current_user:
            self.current_user = VKUser(id=user_id, first_name=vk_user.first_name, last_name=vk_user.last_name)
            self.DB.insert_vk_user(self.current_user)
            self.current_user = self.DB.select_vk_users_data(user_id)
        self.send_msg(user_id, MESSAGES['SEARCHING'])
        if not use_new_settings:
            self.bot_settings.reset_settings(vk_user.age)
        search_res = self.vk_core.search_users(age_from=self.bot_settings.age_from, age_to=self.bot_settings.age_to,
                                               city=vk_user.city_id, sex=vk_user.sex)
        self.found_users = search_res.get('items')
        self.send_keyboard(user_id, self.working_keyboard)
        self.send_next_found_person(user_id, self.found_users)

    @bot_exception_logger(LOGGER_PATH, exc_info=True)
    def settings_increase_age(self, user_id: int) -> None:
        """
        Увеличивает диапазон поиска.
        Параметры:
            user_id (int): ID пользователя чат-бота.
        """
        self.bot_settings.increase_age_to()
        self.bot_settings.correct_age_range()
        self.send_msg(user_id, f"⚙ Диапазон поиска: 🔄 "
                               f"от {self.bot_settings.age_from} до {self.bot_settings.age_to}")
        self.send_inline_keyboard(user_id, self.new_search_keyboard, MESSAGES['NEW_SEARCH'])

    @bot_exception_logger(LOGGER_PATH, exc_info=True)
    def settings_decrease_age(self, user_id) -> None:
        """
        Уменьшает диапазон поиска.
        Параметры:
            user_id (int): ID пользователя чат-бота.
        """
        self.bot_settings.decrease_age_from()
        self.bot_settings.correct_age_range()
        self.send_msg(user_id, f"⚙ Диапазон поиска: 🔄 "
                               f"от {self.bot_settings.age_from} до {self.bot_settings.age_to}")
        self.send_inline_keyboard(user_id, self.new_search_keyboard, MESSAGES['NEW_SEARCH'])

    @bot_exception_logger(LOGGER_PATH, exc_info=True)
    def settings_ignore_blacklist(self, user_id) -> None:
        """
        Переключает использование черного списка.
        Параметры:
            user_id (int): ID пользователя чат-бота.
        """
        self.bot_settings.switch_use_blacklist()
        if self.bot_settings.use_blacklist:
            self.send_msg(user_id, "⚙ Блэклист включен ☀")
        else:
            self.send_msg(user_id, "⚙ Блэклист выключен 🌥")
        self.send_inline_keyboard(user_id, self.new_search_keyboard, MESSAGES['NEW_SEARCH'])

    @bot_exception_logger(LOGGER_PATH, exc_info=True)
    def settings_reset(self, user_id) -> None:
        """
        Сбрасывает настройки бота.
        Параметры:
            user_id (int): ID пользователя чат-бота.
        """
        age = self.vk_core.vk_bot_user.age
        if age:
            self.bot_settings.reset_settings(age)
        else:
            self.bot_settings.reset_settings()
        self.send_msg(user_id, "⚙ Настройки сброшены 🌀")
        self.send_inline_keyboard(user_id, self.new_search_keyboard, MESSAGES['NEW_SEARCH'])
