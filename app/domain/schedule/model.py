from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, engine


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String)
    start_time= Column(DateTime)
    end_time= Column(DateTime)
    room_id = Column(Integer, ForeignKey('rooms.id'))

    room = relationship("Room", back_populates="schedules")
    participants = relationship("Participant", back_populates="schedule", cascade="all, delete-orphan")
