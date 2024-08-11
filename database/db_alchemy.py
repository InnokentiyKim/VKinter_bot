from database.db_core import Base, Session, engine
from models.vk_user import VKUser
from models.favourites import Favourites
from models.blacklist import BlackList


class DBManager:
    def __init__(self):
        self.engine = engine
        self._session = Session()
        Base.metadata.create_all(engine)

    def init_defaults(self):
        with self._session as session:
            user_1 = VKUser(id=2132423, first_name="Vasya")
            user_2 = VKUser(id=3523523, first_name="Petya")
            user_3 = VKUser(id=2352362, first_name="Kolya")
            session.add_all([user_1, user_2, user_3])
            session.flush()
            favourites_1 = Favourites(id=23532423, vk_user_id=user_1.id)
            favourites_2 = Favourites(id=46532423, vk_user_id=user_1.id)
            favourites_3 = Favourites(id=67332423, vk_user_id=user_2.id)
            favourites_4 = Favourites(id=34324243, vk_user_id=user_2.id)
            favourites_5 = Favourites(id=86722423, vk_user_id=user_2.id)
            blacked_user_1 = BlackList(id=1115885, user_id=user_1.id)
            blacked_user_2 = BlackList(id=1658544, user_id=user_2.id)
            blacked_user_3 = BlackList(id=23532423, user_id=user_2.id)
            session.add_all(
                [
                    favourites_1,
                    favourites_2,
                    favourites_3,
                    favourites_4,
                    favourites_5,
                    blacked_user_1,
                    blacked_user_2,
                    blacked_user_3,
                ]
            )
            session.commit()
