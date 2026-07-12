from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.schedule.schema import ScheduleCreateRequest
from app.domain.schedule import repository
from app.domain.schedule.model import Schedule
from app.domain.participant.model import Participant
from app.core.exceptions import (InvalidTimeRangeException, RoomNotFoundException, UserNotFoundException
                                 , ScheduleConflictException, ParticipantConflictException, ScheduleNotFoundException
                                 )


def create_schedule(db: Session, request: ScheduleCreateRequest) -> Schedule:
    if request.start_time < datetime.now():
        raise InvalidTimeRangeException("시작시간이 현재 시간보다 앞섭니다.")

    room = repository.get_room_by_id(db, request.room_id)
    if not room:
        raise RoomNotFoundException()


    unique_user_ids = list(set(request.participants))
    users = repository.get_users_by_ids(db, unique_user_ids)

    if len(users) != len(unique_user_ids):
        raise UserNotFoundException()


    room_conflicts = repository.get_room_conflicting_schedules(
        db, request.room_id, request.start_time, request.end_time
    )
    if room_conflicts:
        raise ScheduleConflictException()


    participant_conflicts = repository.get_participant_conflicts(
        db, unique_user_ids, request.start_time, request.end_time
    )
    if participant_conflicts:
        raise ParticipantConflictException()


    new_schedule = Schedule.create(
        name=request.name,
        start_time=request.start_time,
        end_time=request.end_time,
        room=room,
        participant_count=len(unique_user_ids)
    )


    for user in users:
        participant = Participant.create(user=user,
                                         start_time=request.start_time,
                                         end_time=request.end_time)
        new_schedule.participants.append(participant)


    return repository.save_schedule(db, new_schedule)

def get_schedule(db: Session, schedule_id: int) -> Schedule:
    schedule = repository.get_schedule_with_details(db, schedule_id)

    if not schedule:
        raise ScheduleNotFoundException()

    return schedule