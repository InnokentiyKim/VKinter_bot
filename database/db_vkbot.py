from sqlalchemy.orm import selectinload
from sqlalchemy import select
from database.db_core import Base, Session, engine
from models.vk_user import VKUser, Favourites, BlackList


class DBManager:
    def __init__(self):
        self.engine = engine
        self._session = Session()
        Base.metadata.create_all(self.engine)

    def insert_vk_user(self, vk_user_id: int, first_name: str = None) -> bool:
        try:
            with self._session as session:
                session.add(VKUser(id=vk_user_id, first_name=first_name))
                session.commit()
                return True
        except ConnectionError:
            print("Ошибка подключения к базе данных")
        return False

    def insert_favourites(self, favourites_id: int, vk_user) -> bool:
        try:
            with self._session as session:
                session.add(Favourites(id=favourites_id, vk_user=vk_user))
                session.commit()
                return True
        except ConnectionError:
            print("Ошибка подключения к базе данных")
        return False

    def insert_blacklist(self, blacklist_id: int, vk_user) -> bool:
        try:
            with self._session as session:
                session.add(BlackList(id=blacklist_id, vk_user=vk_user))
                session.commit()
                return True
        except ConnectionError:
            print("Ошибка подключения к базе данных")
        return False

    def select_vk_user(self, vk_user_id: int) -> VKUser | None:
        try:
            with self._session as session:
                query = (
                    select(VKUser).filter(VKUser.id == vk_user_id)
                )
                query_result = session.execute(query).scalars().first()
                return query_result
        except ConnectionError:
            print("Ошибка подключения к базе данных")
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
        except ConnectionError:
            print("Ошибка подключения к базе данных")
        return None
