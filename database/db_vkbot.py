from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError
from database.db_core import Base, Session, engine
from models.vk_user import VKUser, Favourites, BlackList
from bot_logging.bot_logging import error_logger


class DBManager:
    """
    Класс, используемый для управления базой данных VK пользователей.
    Этот класс предоставляет методы для вставки VK пользователей в базу данных,
    вставки их избранных и черных списков, и получения данных VK пользователей.
    Атрибуты:
        engine (sqlalchemy.engine.Engine): Объект базы данных.
        _session (sqlalchemy.orm.Session): Объект сессии базы данных.
    """
    def __init__(self):
        self.engine = engine
        self._session = Session()
        Base.metadata.create_all(self.engine)

    def insert_vk_user(self, vk_user) -> bool:
        """
        Вставляет VK пользователя в базу данных.
        Аргументы:
            vk_user (VKUser): VK пользователь, который будет вставлен.
        Возвращает:
            bool: True, если пользователь был успешно вставлен, False в противном случае.
        Вызывает:
            IntegrityError: Если пользователь уже существует в базе данных.
            DetachedInstanceError: Если пользователь неправильно присоединен к сессии.
        """
        if isinstance(vk_user, VKUser):
            try:
                with self._session as session:
                        session.add(vk_user)
                        session.commit()
                        return True
            except IntegrityError as integrity_error:
                error_logger.error(integrity_error)
            except DetachedInstanceError as detached_instance_error:
                error_logger.error(detached_instance_error)
            except Exception as error:
                error_logger.error(error)
        return False

    def insert_favourites(self, favourites: dict, vk_user: VKUser) -> bool | None:
        """
        Вставляет избранных VK пользователя в базу данных.
        Аргументы:
            favourites (dict): Словарь, содержащий избранного пользователя.
            vk_user (VKUser): Сам VK пользователь.
        Возвращает:
            bool: True, если избранный был успешно вставлен, False в противном случае.
        Вызывает:
            IntegrityError: Если избранный уже существуют в базе данных.
            DetachedInstanceError: Если пользователь неправильно присоединен к сессии.
            ValueError: Если словарь избранных пуст или недействителен.
        """
        if isinstance(vk_user, VKUser):
            try:
                with self._session as session:
                    session.add(
                        Favourites(id=favourites['user_id'], first_name=favourites['first_name'],
                                   last_name=favourites['last_name'],  vk_user=vk_user))
                    session.commit()
                    return True
            except IntegrityError as integrity_error:
                error_logger.error(integrity_error)
                return False
            except DetachedInstanceError as detached_instance_error:
                error_logger.error(detached_instance_error)
            except Exception as error:
                error_logger.error(error)
        return None

    def insert_blacklist(self, banned: dict, vk_user) -> bool | None:
        """
        Вставляет пользователя в черный список базы данных для последующего его исплючения из поиска.
        Аргументы:
            vk_user (VKUser): VK пользователь
            blacklisted_user (VKUser): VK пользователь, который добавляется в черный список.
        Возвращает:
            bool: True, если пользователь был успешно добавлен в черный список, False в противном случае.
        Вызывает:
            IntegrityError: Если пользователь уже существует в черном списке.
            DetachedInstanceError: Если один из пользователей неправильно присоединен к сессии.
        """
        if isinstance(vk_user, VKUser):
            try:
                with self._session as session:
                    session.add(
                        BlackList(id=banned['user_id'], first_name=banned['first_name'],
                                  last_name=banned['last_name'], vk_user=vk_user))
                    session.commit()
                    return True
            except IntegrityError as integrity_error:
                error_logger.error(integrity_error)
                return False
            except DetachedInstanceError as detached_instance_error:
                error_logger.error(detached_instance_error)
            except Exception as error:
                error_logger.error(error)
        return None

    def select_vk_user(self, vk_user_id: int) -> VKUser | None:
        """
        Выбирает VK пользователя из базы данных по его VK ID.
        Аргументы:
            vk_id (int): ID пользователя, которого нужно выбрать.
        Возвращает:
            Optional[VKUser]: Выбранный VK пользователь, или None, если не найден.
        """
        try:
            with self._session as session:
                query = (
                    select(VKUser).filter(VKUser.id == vk_user_id)
                )
                query_result = session.execute(query).scalars().first()
                return query_result
        except Exception as error:
            error_logger.error(error)
        return None

    def select_vk_users_data(self, vk_user_id: int) -> VKUser | None:
        """
        Выгружает данные пользователя из базы данных по его ID.
        Аргументы:
            vk_id (int): ID пользователя, которого нужно выбрать.
        Возвращает:
            Optional[VKUser]: Выбранный пользователь, или None, если не найден.
        """
        try:
            with self._session as session:
                query = (
                    select(VKUser).filter(VKUser.id == vk_user_id)
                    .options(selectinload(VKUser.favourites))
                    .options(selectinload(VKUser.blacklist))
                )
                query_result = session.execute(query).scalars().first()
                return query_result
        except Exception as error:
            error_logger.error(error)
        return None
