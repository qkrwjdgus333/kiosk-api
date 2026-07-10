from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base, engine
from datetime import datetime


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

    @staticmethod
    def __check_time_rule(start_time: datetime, end_time: datetime) -> bool:
        return start_time < end_time

    @classmethod
    def create(cls, user: "User", start_time: datetime, end_time: datetime) -> 'Participant':

        if not Participant.__check_time_rule(start_time, end_time):
            raise ValueError("참여 시작 시간은 종료 시간보다 빨라야 합니다.")

        return cls(
            user_id=user.id,
            name=user.name,
            start_time=start_time,
            end_time=end_time
        )