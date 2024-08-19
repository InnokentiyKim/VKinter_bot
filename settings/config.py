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
    'HELLO': 'привет',
    'GOODBYE': 'пока',
    'HELP': 'инструкция',
    'CONFIG': 'настройки',
    'NEXT': 'следующий',
    'TO_FAVOURITES': 'добавить в избранное',
    'TO_BLACKLIST': 'добавить в черный список',
    'SHOW_FAVOURITES': 'избранное',
    'DECREASE_AGE': 'снизить возраст поиска',
    'INCREASE_AGE': 'поднять возраст поиска',
    'IGNORE_BLACKLIST': 'игнорировать черный список',
    'RESET_SETTINGS': 'сбросить все настройки',
    'NEW_SEARCH': 'начать новый поиск',
    'ABOUT': 'о боте',
}

GENDER = {'ANY': 0, 'WOMAN': 1, 'MAN': 2, }
STATUS = {'NOT_MERRIED': 1, 'COMPLICATED': 5,
          'ACTIVE': 6, 'MERRIED_OFF': 8, }
