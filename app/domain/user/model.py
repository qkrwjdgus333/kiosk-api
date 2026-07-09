from sqlalchemy import Column, Integer, String
from app.database import Base, engine


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)