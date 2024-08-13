import vk_api
from datetime import datetime
from settings.config import settings


class VKBotUser:
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.sex = 0
        self.relation = 0
        self.city_id = 1
        self.city = None
        self.bdate = None
        self.age = None

    def get_vk_user(self) -> dict:
        users_info = {'id': self.id, 'first_name': self.first_name, 'last_name': self.last_name, 'sex': self.sex,
                      'relation': self.relation, 'city': self.city, 'bdate': self.bdate, 'age': self.age, }
        return users_info

    def set_vk_user(self, user_id: int, info: dict) -> None:
        self.id = user_id
        self.first_name = info.get('first_name')
        self.last_name = info.get('last_name')
        self.sex = info.get('sex')
        self.relation = info.get('relation')
        self.city_id = info['city']['id'] if 'city' in info else None
        self.city = info['city']['title'] if 'city' in info else None
        self.bdate = info.get('bdate')
        self.age = datetime.now().year - int(self.bdate.split('.')[2]) if self.bdate else None


class VKCore:
    def __init__(self, vk_api_token):
        self.vk = vk_api.VkApi(token=vk_api_token).get_api()
        self.vk_bot_user = VKBotUser()
        self.fields = "bdate,city,contancts,interests,photo_400_orig"

    def get_profiles_info(self, user_id: int) -> bool:
        try:
            info = self.vk.account.getProfileInfo(user_id=user_id)
            self.vk_bot_user.set_vk_user(user_id, info)
            return True
        except vk_api.exceptions.ApiError:
            print(f"Error while getting users {user_id} profile info")
            return False

    def _get_age_range(self, users_age: int, min_lower_age: int = 2, max_upper_age: int = 2) -> tuple:
        return users_age - min_lower_age, users_age + max_upper_age

    def search_users(self, query: str = '', count: int = settings.SEARCH_LIMIT,
                     age: int = 20, city: int = 1, sex: int = 1, has_photo: int = 1) -> list:
        age_from, age_to = self._get_age_range(age)
        found_users = self.vk.users.search(q=query, count=count, age_from=age_from, age_to=age_to,
                                            has_photo=has_photo, fields=self.fields, city=city, sex=sex)
        return found_users

    def get_users_photos(self, owner_id: int, album_id: str = 'profile') -> list:
        photos = self.vk.photos.get(owner_id=owner_id, album_id=album_id, extended=1)
        return photos
