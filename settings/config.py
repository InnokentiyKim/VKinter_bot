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

COMMANDS = {
    'START': 'начать',
    'HELP': 'инструкция',
    'MENU': 'меню',
    'NEXT': 'следующий',
    'FAVOURITES': 'добавить в избранное',
    'BLACKLIST': 'добавить в черный список',
}

GENDER = {'любой': 0, 'женщина': 1, 'мужчина': 2, }
STATUS = {'NOT_MERRIED': 1, 'DATING': 2, 'ENGAGED': 3, 'MERRIED': 4, 'COMPLICATED': 5,
          'ACTIVE': 6, 'IN_LOVE': 7, 'MERRIED_OFF': 8, }
