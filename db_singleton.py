from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

class SQLAlchemySessionSingleton:
    _engine = None
    _SessionLocal = None

    @classmethod
    def initialize(cls, db_url):
        if cls._engine is None:
            cls._engine = create_engine(db_url, echo=True)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
            Base.metadata.bind = cls._engine

    @classmethod
    def get_session(cls):
        if cls._SessionLocal is None:
            raise Exception("Engine is not initialized. Call initialize() first.")
        return cls._SessionLocal()
