from sqlalchemy import Column, Integer, String

from app.database import Base, engine


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind = engine)