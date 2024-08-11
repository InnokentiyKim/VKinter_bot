import os
from dotenv import load_dotenv


load_dotenv()
SEARCH_LIMIT = 1000


class Settings:
    def __init__(self):
        self.vk_token = os.getenv('TOKEN')
        self.vk_api_token = os.getenv('API_TOKEN')
        self.vk_group_ID = os.getenv('GROUP_ID')
        self.search_limit = SEARCH_LIMIT

    @property
    def token(self):
        return self.vk_token

    @property
    def api_token(self):
        return self.vk_api_token

    @property
    def group_id(self):
        return self.vk_group_ID


settings = Settings()

GENDER = {'любой': 0, 'женщина': 1, 'мужчина': 2, }
STATUS = {'не женат': 1, 'встречается': 2, 'помолвлен(-а)': 3, 'женат (замужем)': 4, 'всё сложно': 5,
          'в активном поиске': 6, 'влюблён(-а)': 7, 'в гражданском браке': 8, }
