from settings.config import settings


STICKS = {
    'HELLO': 105,
    'GOODBYE': 110,
    'SLEEP': 97,
    'START': 102,
    'MISUNDERSTAND': 116,
    'HELP': 121,
}

MESSAGES = {
    'START': "Начать",
    'HELP': "Добро пожаловать в VKinder!\n"
            "Я помогу вам найти новые знакомства.\n"
            "Нажмите на кнопку 'Начать' для поиска людей\n",
    'ABOUT': f"Бот VKinder был разработан с целью помочь найти новые знакомства.\n"
             f"Бот учитывает ваш город, возраст и пол.\n"
             f"Все данные берутся из вашего профиля.\n"
             f"Версия бота: {settings.VERSION}\n"
             f"Автор: {settings.AUTHOR}\n" 
             f"Все права защищены.\n"
             f"GitHub: https://github.com/InnCent/VKinder\n",
}
