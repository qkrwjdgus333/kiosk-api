from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base, engine


class Schedule(Base):
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time= Column(DateTime)
    end_time= Column(DateTime)
    room_id = Column(Integer, ForeignKey('room.id'))

Base.metadata.create_all(engine)