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
