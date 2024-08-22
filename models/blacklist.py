from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db_core import Base
from typing import Optional


class BlackList(Base):
    """
    Представляет сущность "черный список" в базе данных.
    Атрибуты:
        id (int): Уникальный идентификатор записи в черном списке.
        first_name (str): Имя человека, внесенного в черный список.
        last_name (str): Фамилия человека, внесенного в черный список.
        vk_user_id (int): Внешний ключ - идентификатор VK пользователя.
    Примечания:
        Этот класс является моделью SQLAlchemy, представляющей таблицу в базе данных.
        Он устанавливает отношение "многие ко многим" между пользователями и элементами.
    """
    __tablename__ = 'blacklist'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column()
    vk_user_id: Mapped[int] = mapped_column(ForeignKey('vk_user.id', ondelete='CASCADE'))
    vk_user: Mapped['VKUser'] = relationship(back_populates='blacklist')
