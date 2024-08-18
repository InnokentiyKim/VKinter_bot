import vk_api
from settings.config import settings, STATUS
from source.vk_entity import VKBotUser, VKFoundUser


class VKCore:
    def __init__(self, vk_api_token):
        self.vk = vk_api.VkApi(token=vk_api_token).get_api()
        self.vk_bot_user = VKBotUser()
        self.fields = "bdate,city,contancts,interests,is_closed"

    def get_profiles_info(self, user_id: int) -> bool:
        try:
            info = self.vk.account.getProfileInfo(user_id=user_id)
            self.vk_bot_user.set_vk_user(user_id, info)
            return True
        except vk_api.exceptions.ApiError as ApiError:
            print(f"Error while getting users {user_id} profile info. {ApiError}")
            return False

    @staticmethod
    def _get_age_range(users_age: int, min_lower_age: int = 2, max_upper_age: int = 2) -> tuple:
        return users_age - min_lower_age, users_age + max_upper_age

    def search_users(self, query: str = '', count: int = settings.SEARCH_LIMIT,
                     age: int = 20, city: int = 1, sex: int = 1, has_photo: int = 1) -> dict:
        sex = 2 if sex == 1 else 1
        age_from, age_to = self._get_age_range(age)
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
        except vk_api.exceptions.ApiError:
            print(f"Error while getting users {owner_id} photos")
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
