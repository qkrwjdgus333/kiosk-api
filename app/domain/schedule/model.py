from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.exceptions import InvalidTimeRangeException, RoomCapacityExceededException
from app.database import Base, engine


class Schedule(Base):
    __tablename__ = 'schedules'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    start_time= Column(DateTime)
    end_time= Column(DateTime)
    room_id = Column(Integer, ForeignKey('rooms.id'))

    room = relationship("Room", back_populates="schedules")
    participants = relationship("Participant", back_populates="schedule", cascade="all, delete-orphan")

    @staticmethod
    def __check_time_rule(start_time: datetime, end_time: datetime) -> bool:
        return start_time < end_time

    @staticmethod
    def __check_room_capacity(room: "Room", participant_count: int) -> bool:
        """회의실 수용 인원 규칙 검증"""
        return  participant_count <= room.capacity

    @classmethod
    def create(cls, name: str, start_time: datetime, end_time: datetime, room: "Room",participant_count: int) -> 'Schedule':
        if not Schedule.__check_time_rule(start_time, end_time):
            raise InvalidTimeRangeException("시작 시간은 종료 시간보다 빨라야 합니다.")

        if not Schedule.__check_room_capacity(room, participant_count):
            raise RoomCapacityExceededException(f"회의실 수용 인원({room.capacity}명)을 초과했습니다.")

        return Schedule(name=name, start_time=start_time, end_time=end_time, room=room)