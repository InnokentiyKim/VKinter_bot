import unittest
from settings.config import settings

class TestSettings(unittest.TestCase):
    def test_settings_dsn(self):
        # Проверка корректности сборки DSN
        expected_dsn = f"{settings.DIALECT}://{settings.USERNAME}:{settings.PASSWORD}@{settings.URL}:{settings.PORT}/{settings.DB_NAME}"
        self.assertEqual(settings.DSN, expected_dsn)

if __name__ == '__main__':
    unittest.main()
