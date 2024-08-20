from source.vk_bot_main import VKBot
from bot_logging.bot_logging import error_logger


def main():
    while True:
        try:
            vk_bot = VKBot()
            print("Бот запущен...")
            vk_bot.start_pooling()
        except Exception as error:
            error_logger.error(error)
            continue


if __name__ == '__main__':
    main()
