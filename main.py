from source.vk_bot import VKBot
from database.db_alchemy import DBManager


def main():
    vk_bot = VKBot()
    DB = DBManager()
    DB.init_defaults()
    user_data = DB.select_vk_users_data(2423532)
    print(user_data)
    for favourite in user_data.favourites:
        print(favourite.id)
    for blacklist in user_data.blacklist:
        print(blacklist.id)
    print("Бот запущен...")
    vk_bot.start_pooling()


if __name__ == '__main__':
    main()
