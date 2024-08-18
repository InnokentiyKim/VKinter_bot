from source.vk_bot_main import VKBot


def main():
    while True:
        try:
            vk_bot = VKBot()
            print("Бот запущен...")
            vk_bot.start_pooling()
        except Exception:
            print("Ошибка в работе бота. Перезапускаю...")
            continue


if __name__ == '__main__':
    main()
