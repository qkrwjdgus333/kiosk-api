from sqlalchemy.orm import Session
from datetime import datetime

from app.domain.schedule.model import Schedule
from app.domain.room.model import Room
from app.domain.user.model import User
from app.domain.participant.model import Participant

def get_room_by_id(db: Session, room_id: int) -> Room | None:
    return db.query(Room).filter(Room.id == room_id).first()

def get_room_confilicting_schedule(db: Session, room_id: int, start_time: datetime, end_time: datetime) -> list[Schedule]:
    return db.query(Schedule).filter(
        Schedule.room_id == room_id,
        Schedule.start_time < end_time,
        Schedule.end_time > start_time,
    ).all()

def get_participant_conflicts(db: Session, user_ids: list[int], start_time: datetime, end_time: datetime) -> list[Participant]:
    return db.query(Participant).filter(
        Participant.user_id.in_(user_ids),
        Participant.start_time < end_time,
        Participant.end_time > start_time
    ).all()

def save_schedule(db: Session, schedule: Schedule) -> Schedule:
    """
    새로운 일정을 데이터베이스에 영속화(저장)합니다.
    이때 양방향 참조로 연결된 Participant 객체들도 cascade 속성에 의해 자동으로 함께 저장됩니다.
    """
    db.add(schedule)
    db.commit()
    db.refresh(schedule) # DB에서 생성된 ID(PK) 등을 객체에 동기화
    return schedule

def get_schedule_with_details(db: Session, schedule_id: int) -> Schedule | None:
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()



