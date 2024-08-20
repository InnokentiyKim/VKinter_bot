import vk_api
from settings.config import settings, GENDER
from source.vk_entity import VKBotUser
from bot_logging.bot_logging import error_logger, bot_exception_logger, LOGGER_PATH


class VKCore:
    def __init__(self, vk_api_token):
        self.vk = vk_api.VkApi(token=vk_api_token).get_api()
        self.vk_bot_user = VKBotUser()
        self.fields = "bdate,city,contancts,interests,relation,is_closed"

    def get_profiles_info(self, user_id: int) -> bool:
        try:
            info = self.vk.account.getProfileInfo(user_id=user_id)
            self.vk_bot_user.set_vk_user(user_id, info)
            return True
        except Exception as error:
            error_logger.error(error)
            return False

    @staticmethod
    def _get_age_range(users_age: int, min_lower_age: int = 2, max_upper_age: int = 2) -> tuple:
        return users_age - min_lower_age, users_age + max_upper_age

    @bot_exception_logger(LOGGER_PATH)
    def search_users(self, query: str = '', count: int = settings.SEARCH_LIMIT,
                     age_from: int = 20, age_to: int = 22, city: int = 1, sex: int = 1, has_photo: int = 1) -> dict:
        sex = GENDER['MAN'] if sex == GENDER['WOMAN'] else GENDER['WOMAN']
        found_users = self.vk.users.search(q=query, count=count, age_from=age_from, age_to=age_to,
                                           has_photo=has_photo, fields=self.fields, city=city, sex=sex)
        return found_users

    def get_users_photos(self, owner_id: int, album_id: str = 'profile', is_closed: bool = False) -> list[dict] | None:
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
