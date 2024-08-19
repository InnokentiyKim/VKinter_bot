from vk_api.longpoll import VkLongPoll
from time import sleep

TIMEOUT = 5
MIN_AGE = 16
MAX_AGE = 60

class CoreVkLongPoll(VkLongPoll):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def listen(self):
        while True:
            try:
                for event in self.check():
                    yield event
            except Exception as error:
                print(error)
                sleep(TIMEOUT)
                continue


class BotSettings:
    def __init__(self):
        self.age_from = 20
        self.age_to = 22
        self.use_blacklist = True

    def get_ages(self) -> tuple:
        return self.age_from, self.age_to

    def set_ages(self, age_from, age_to) -> None:
        self.age_from = age_from
        self.age_to = age_to

    def set_use_blacklist(self) -> None:
        if self.use_blacklist:
            self.use_blacklist = False
        else:
            self.use_blacklist = True

    def correct_age_range(self) -> None:
        if self.age_from < MIN_AGE:
            self.age_from = MIN_AGE
        if self.age_to > MAX_AGE:
            self.age_to = MAX_AGE

    def reset_settings(self, user_age: int, diff: int = 1) -> None:
        self.age_from = user_age - diff
        self.age_to = user_age + diff
        self.use_blacklist = True
        self.correct_age_range()
