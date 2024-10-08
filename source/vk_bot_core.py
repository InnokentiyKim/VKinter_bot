from vk_api.longpoll import VkLongPoll
from time import sleep
from bot_logging.bot_logging import error_logger, bot_exception_logger, LOGGER_PATH

TIMEOUT = 5
MIN_AGE = 16
MAX_AGE = 60

class CoreVkLongPoll(VkLongPoll):
    """
    Класс, реализующий лонгпулл, используемый для работы бота.
    Атрибуты:
        super().__init__(*args, **kwargs)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def listen(self):
        """
        Генератор, возвращающий события из лонгпулла.
        Возвращает: Event - события из лонгпулла.
        """
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as error:
                error_logger.error(error)
                sleep(TIMEOUT)
                continue


class BotSettings:
    """
    Класс с настройками бота.
    Атрибуты:
        age_from (int): Нижняя граница возраста.
        age_to (int): Верхняя граница возраста.
        use_blacklist (bool): Использовать ли черный список.
    """
    def __init__(self):
        self.age_from = 20
        self.age_to = 22
        self.use_blacklist = True

    def get_ages(self) -> tuple:
        """
        Возвращает кортеж с границами возраста.
        """
        return self.age_from, self.age_to

    @bot_exception_logger(LOGGER_PATH)
    def decrease_age_from(self, age: int = 1):
        """
        Уменьшает нижнюю границу возраста.
        Параметры:
            age (int): Количество лет для уменьшения (по умолчанию 1).
        Возвращает: None
        """
        self.age_from -= age

    @bot_exception_logger(LOGGER_PATH)
    def increase_age_to(self, age: int = 1):
        """
        Увеличивает верхнюю границу возраста.
        Параметры:
            age (int): Количество лет для увеличения (по умолчанию 1).
        Возвращает: None
        """
        self.age_to += age

    def set_ages(self, age_from, age_to) -> None:
        """
        Устанавливает границы возраста.
        Возвращает: None
        """
        self.age_from = age_from
        self.age_to = age_to

    @bot_exception_logger(LOGGER_PATH)
    def switch_use_blacklist(self) -> None:
        """
        Переключает использование черного списка.
        Возвращает: None
        """
        if self.use_blacklist:
            self.use_blacklist = False
        else:
            self.use_blacklist = True

    def correct_age_range(self) -> None:
        """
        Проверяет и устанавливает корректность границ возраста.
        Возвращает: None
        """
        if self.age_from < MIN_AGE:
            self.age_from = MIN_AGE
        if self.age_to > MAX_AGE:
            self.age_to = MAX_AGE

    @bot_exception_logger(LOGGER_PATH)
    def reset_settings(self, user_age: int = 20, diff: int = 1) -> None:
        """
        Сбрасывает настройки бота.
        Параметры:
            user_age (int): Возраст пользователя.
            diff (int): Разница в возрасте.
        Возвращает: None
        """
        self.age_from = user_age - diff
        self.age_to = user_age + diff
        self.use_blacklist = True
        self.correct_age_range()
