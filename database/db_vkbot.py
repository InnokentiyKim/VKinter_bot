from sqlalchemy.orm import selectinload
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError
from database.db_core import Base, Session, engine
from models.vk_user import VKUser, Favourites, BlackList
from bot_logging.bot_logging import error_logger


class DBManager:
    def __init__(self):
        self.engine = engine
        self._session = Session()
        Base.metadata.create_all(self.engine)

    def insert_vk_user(self, vk_user) -> bool:
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
