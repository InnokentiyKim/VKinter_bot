import vk_api
from datetime import datetime
from settings.config import settings


class VKCore:
    def __init__(self, vk_api_token):
        self.vk = vk_api.VkApi(token=vk_api_token).get_api()
        self.id = None
        self.first_name = None
        self.last_name = None
        self.sex = 0
        self.relation = 0
        self.city = None
        self.bdate = None
        self.age = None
        self.photo = None
        self.phone = None
        self.fields = "first_name,last_name,sex,relation,city,bdate,photo_200,phone"

    def _get_age_range(self, user_age: int, start_age: int, end_age: int, ) -> tuple:
        pass

    def get_profiles_info(self, user_id: int) -> None:
        info = self.vk.account.getProfileInfo(user_id=user_id)
        self.id = user_id
        self.first_name = info.get('first_name')
        self.last_name = info.get('last_name')
        self.sex = info.get('sex')
        self.relation = info.get('relation')
        self.city = info['city']['title'] if 'city' in info else None
        self.bdate = info.get('bdate')
        self.photo = info.get('photo_200')
        self.phone = info.get('phone')
        self.age = datetime.now().year - int(self.bdate.split('.')[2]) if self.bdate else None

    def search_users(self, search_request: str='', count: int=settings.SEARCH_LIMIT, fields: str='') -> list:
        return self.vk.users.search(q=search_request, count=5)
