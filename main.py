from source.vk_bot_main import VKBot
from time import sleep


def main():
    try:
        vk_bot = VKBot()
        print("Бот запущен...")
        vk_bot.start_pooling()
    except Exception:
        sleep(3)
        main()


if __name__ == '__main__':
    main()
