from datetime import datetime
from sqlalchemy.orm import Session

from app.domain.schedule.schema import ScheduleCreateRequest, ScheduleUpdateRequest
from app.domain.schedule import repository
from app.domain.schedule.model import Schedule
from app.domain.participant.model import Participant
from app.core.exceptions import *


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


from app.domain.schedule.schema import ScheduleUpdateRequest


def update_schedule(db: Session, schedule_id: int, request: ScheduleUpdateRequest) -> Schedule:
    schedule = repository.get_schedule_with_details(db, schedule_id)
    if not schedule:
        raise ScheduleNotFoundException()

    update_data = request.model_dump(exclude_unset=True)
    if not update_data:
        return schedule

    new_room_id = update_data.get("room_id", schedule.room_id)
    new_start = update_data.get("start_time", schedule.start_time)
    new_end = update_data.get("end_time", schedule.end_time)

    if new_start >= new_end:
        raise InvalidTimeRangeException("시작 시간은 종료 시간보다 빨라야 합니다.")

    if "room_id" in update_data:
        new_room = repository.get_room_by_id(db, new_room_id)
        if not new_room:
            raise RoomNotFoundException()
        if len(schedule.participants) > new_room.capacity:
            raise RoomCapacityExceededException(f"새로운 회의실의 수용 인원({new_room.capacity}명)을 초과합니다.")

    if "start_time" in update_data or "end_time" in update_data or "room_id" in update_data:
        room_conflicts = repository.get_room_conflicting_schedules(
            db, new_room_id, new_start, new_end, exclude_schedule_id=schedule.id
        )
        if room_conflicts:
            raise ScheduleConflictException()


    for key, value in update_data.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)
    return schedule