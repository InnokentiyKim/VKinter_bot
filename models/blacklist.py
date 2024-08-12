from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from database.db_core import Base


class BlackList(Base):
    __tablename__ = 'blacklist'

    id: Mapped[int] = mapped_column(primary_key=True)
    vk_user_id: Mapped[int] = mapped_column(ForeignKey('vk_user.id', ondelete='CASCADE'))
    vk_user: Mapped['VKUser'] = relationship(back_populates='blacklist')
