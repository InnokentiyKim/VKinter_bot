from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional
from database.db_core import Base
from models.favourites import Favourites
from models.blacklist import BlackList


class VKUser(Base):
    """
    Представляет сущность пользователя VK в базе данных.
    Атрибуты:
        id (int): Уникальный идентификатор пользователя VK.
        first_name (str): Имя пользователя VK.
        last_name (str): Фамилия пользователя VK.
    Примечания:
        Этот класс является моделью SQLAlchemy, представляющей таблицу в базе данных.
        Он хранит информацию о пользователях VK, взаимодействовавших с приложением.
    """
    __tablename__ = 'vk_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(default=f"user {id}")
    last_name: Mapped[Optional[str]] = mapped_column()
    favourites: Mapped[list['Favourites']] = relationship(back_populates='vk_user')
    blacklist: Mapped[list['BlackList']] = relationship(back_populates='vk_user')
