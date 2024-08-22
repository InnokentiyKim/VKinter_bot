from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.db_core import Base
from typing import Optional


class Favourites(Base):
    """
    Представляет сущность "избранное" в базе данных.
    Атрибуты:
        id (int): Уникальный идентификатор записи в "избранном".
        vk_user_id (int): Внешний ключ, ссылающийся на пользователя, владеющего "избранным".
        first_name (str): Имя человека, внесенного в "избранные".
        last_name (str): Фамилия человека, внесенного в "избранные".

    Примечания:
        Этот класс является моделью SQLAlchemy, представляющей таблицу в базе данных.
        Он устанавливает отношение "многие ко многим" между пользователями и элементами.
    """
    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_user_id: Mapped[int] = mapped_column(ForeignKey('vk_user.id', ondelete='CASCADE'))
    first_name: Mapped[Optional[str]] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column()
    vk_user: Mapped['VKUser'] = relationship(back_populates='favourites')
