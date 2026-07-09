from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, engine


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    schedule_id = Column(Integer, ForeignKey('schedules.id'))
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

    user = relationship("User", back_populates="participants")
    schedule = relationship("Schedule", back_populates="participants")