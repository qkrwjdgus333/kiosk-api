import datetime

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base, engine
from app.domain.schedule.model import Schedule


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    capacity = Column(Integer, nullable=False)

    schedule = relationship("Schedule", back_populates="room")
