from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from settings.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(url=settings.DSN, echo=True, pool_size=5, max_overflow=2)
Session = sessionmaker(bind=engine, autocommit=False, autoflush=False)
