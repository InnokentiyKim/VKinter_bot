from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from database.db_core import Base
from models.blacklist import BlackList
from models.favourites import Favourites


class VKUser(Base):
    __tablename__ = 'vk_user'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[Optional[str]] = mapped_column(default=f"user {id}")
    favourites: Mapped[List['Favourites']] = relationship(back_populates='vk_user')
    blacklist: Mapped[List['BlackList']] = relationship(back_populates='vk_user')
