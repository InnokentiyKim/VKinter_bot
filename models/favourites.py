from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.db_core import Base
from typing import Optional


class Favourites(Base):
    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_user_id: Mapped[int] = mapped_column(ForeignKey('vk_user.id', ondelete='CASCADE'))
    first_name: Mapped[Optional[str]] = mapped_column()
    last_name: Mapped[Optional[str]] = mapped_column()
    vk_user: Mapped['VKUser'] = relationship(back_populates='favourites')
