from sqlalchemy.orm import selectinload
from sqlalchemy import select
from database.db_core import Base, Session, engine
from models.vk_user import VKUser, Favourites, BlackList


class DBManager:
    def __init__(self):
        self.engine = engine
        self._session = Session()
        Base.metadata.drop_all(self.engine)
        Base.metadata.create_all(self.engine)

    def init_defaults(self):
        with self._session as session:
            user_1 = VKUser(id=2423532, first_name="Vasya")
            user_2 = VKUser(id=4363434, first_name="Petya")
            user_3 = VKUser(id=6324234, first_name="Kolya")
            favourites_1 = Favourites(id=2352362, vk_user=user_1)
            favourites_2 = Favourites(id=3904760, vk_user=user_3)
            favourites_3 = Favourites(id=3985092, vk_user=user_1)
            favourites_4 = Favourites(id=8743533, vk_user=user_2)
            blacklist_1 = BlackList(id=984353234, vk_user=user_1)
            blacklist_2 = BlackList(id=43097503, vk_user=user_2)
            blacklist_3 = BlackList(id=98945345, vk_user=user_3)
            session.add_all(
                [
                    user_1, user_2, user_3,
                    favourites_1, favourites_2, favourites_3, favourites_4,
                    blacklist_1, blacklist_2, blacklist_3
                ]
            )
            session.commit()

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
