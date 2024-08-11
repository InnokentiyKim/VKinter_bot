import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    def __init__(self):
        self.vk_token = os.getenv('TOKEN')
        self.vk_api_token = os.getenv('API_TOKEN')
        self.vk_group_ID = os.getenv('GROUP_ID')

    DB_NAME = os.getenv('DB_NAME')
    DIALECT = os.getenv('DIALECT')
    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    PORT = os.getenv('PORT')
    URL = os.getenv('URL')
    SEARCH_LIMIT = 1000
    VERSION = '1.0.0'
    AUTHOR = 'InnCent'

    @property
    def DSN(self):
        return f"{self.DIALECT}://{self.USERNAME}:{self.PASSWORD}@{self.URL}:{self.PORT}/{self.DB_NAME}"

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
