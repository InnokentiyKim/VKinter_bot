from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database.db_core import Base


class Favourites(Base):
    __tablename__ = 'favourites'

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_user_id: Mapped[int] = mapped_column(ForeignKey('vk_user.id', ondelete='CASCADE'))
    vk_user: Mapped['VKUser'] = relationship(back_populates='favourites')
