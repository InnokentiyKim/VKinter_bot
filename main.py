from source.vk_bot import VKBot
from database.db_vkbot import DBManager


def main():
    vk_bot = VKBot()
    DB = DBManager()
    print("Бот запущен...")
    vk_bot.start_pooling()


if __name__ == '__main__':
    main()
