from source.vk_bot_main import VKBot


def main():
    vk_bot = VKBot()
    print("Бот запущен...")
    vk_bot.start_pooling()


if __name__ == '__main__':
    main()
