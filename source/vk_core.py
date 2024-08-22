import vk_api
from vk_api.exceptions import VkApiError

from settings.config import settings, GENDER
from source.vk_entity import VKBotUser
from bot_logging.bot_logging import error_logger, bot_exception_logger, LOGGER_PATH


class VKCore:
    """
    Основной класс для работы с VK API.
    """
    def __init__(self, vk_api_token):
        """
        Инициализирует объект VKCore.
        Атрибуты:
            vk (vk_api.VkApi): Объект сессии VK API.
            vk_bot_user (source.vk_entity.VKBotUser): Объект пользователя бота.
            fields (str): Список полей, которые необходимо получить.
        """
        self.vk = vk_api.VkApi(token=vk_api_token).get_api()
        self.vk_bot_user = VKBotUser()
        self.fields = "bdate,city,contancts,interests,relation,is_closed"

    def get_profiles_info(self, user_id: int) -> bool:
        """
        Запрашивает информацию о профиле пользователя.
        Параметры:
            user_id (int): ID пользователя.
        Возвращает:
            bool: True, если профиль успешно получен, иначе False.
        """
        try:
            info = self.vk.account.getProfileInfo(user_id=user_id)
            self.vk_bot_user.set_vk_user(user_id, info)
            return True
        except VkApiError as ApiError:
            error_logger.error(ApiError)
            return False
        except Exception as error:
            error_logger.error(error)
            return False

    @bot_exception_logger(LOGGER_PATH)
    def search_users(self, query: str = '', count: int = settings.SEARCH_LIMIT,
                     age_from: int = 20, age_to: int = 22, city: int = 1, sex: int = 1, has_photo: int = 1) -> dict:
        """
        Поиск пользователей.
        Параметры:
            query (str): Запрос при поиске.
            count (int): Количество возвращаемых пользователей.
            age_from (int): Минимальный возраст поиска.
            age_to (int): Максимальный возраст поиска.
            city (int): ID города.
            sex (int): Пол пользователя.
            has_photo (int): Наличие фото.
        Возвращает:
            dict: Словарь с информацией о найденных пользователях.
        """
        sex = GENDER['MAN'] if sex == GENDER['WOMAN'] else GENDER['WOMAN']
        found_users = self.vk.users.search(q=query, count=count, age_from=age_from, age_to=age_to,
                                           has_photo=has_photo, fields=self.fields, city=city, sex=sex)
        return found_users

    def get_users_photos(self, owner_id: int, album_id: str = 'profile', is_closed: bool = False) -> list[dict] | None:
        """
        Запрашивает фотографии пользователей.
        Параметры:
            owner_id (int): ID пользователя.
            album_id (str): ID альбома (по умолчанию - 'profile').
            is_closed (bool): Закрыт ли профиль.
        Возвращает:
            list[dict]: Список с информацией о найденных пользователях.
        """
        try:
            if not is_closed:
                photos = self.vk.photos.get(owner_id=owner_id, album_id=album_id, extended=1, photos_sizes=0)
                best_photos = self._get_best_photos(photos)
                return best_photos
            else:
                return None
        except Exception as error:
            error_logger.error(error)
            return None

    @staticmethod
    def _get_best_photos(found_photos: dict, count: int = 3) -> list[dict]:
        """
        Выбирает лучшие фотографии.
        Параметры:
            found_photos (dict): Словарь с информацией о найденных пользователях.
            count (int): Количество лучших фотографий.
        Возвращает:
            list[dict]: Список с лучшими фотографиями.
        """
        best_photos = []
        if found_photos:
            all_photos = found_photos.get('items')
            for photo in all_photos:
                current_photo = {}
                current_photo['id'] = photo.get('id')
                current_photo['owner_id'] = photo.get('owner_id')
                current_photo['likes'] = photo.get('likes').get('count')
                best_photos.append(current_photo)
            best_photos.sort(key=lambda x: x['likes'], reverse=True)
        return best_photos[:count]
