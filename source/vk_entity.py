from datetime import datetime


class VKBotUser:
    """
    Класс для хранения информации о пользователе VK.
    Атрибуты:
        id (int): ID пользователя VK.
        first_name (str): Имя пользователя.
        last_name (str): Фамилия пользователя.
        sex (int): Пол пользователя.
        relation (int): Семейное положение пользователя.
        city_id (int): ID города пользователя.
        city (str): Название города пользователя.
        bdate (str): Дата рождения пользователя.
        age (int): Возраст пользователя.
    Методы:
        get_vk_user(self): Возвращает словарь с информацией о пользователе VK.
        set_vk_user(self, user_id: int, info: dict): Устанавливает информацию о пользователе VK.
    """
    def __init__(self):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.sex = 0
        self.relation = 0
        self.city_id = 0
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
