from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from settings.config import settings


class Base(DeclarativeBase):
    def __repr__(self):
        cols = []
        for col in self.__table__.columns.keys():
            cols.append(f"{col} = {getattr(self, col)}")
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


engine = create_engine(url=settings.DSN, echo=True, pool_size=5, max_overflow=2)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
