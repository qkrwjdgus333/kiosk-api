from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class RoomInfo(BaseModel):
    id: int = Field(..., description="회의실 ID")
    name: str = Field(..., description="회의실 이름")
    capacity: int = Field(..., description="회의실 최대 수용 인원")

    model_config = ConfigDict(from_attributes=True)

class ParticipantInfo(BaseModel):
    user_id: int = Field(..., description="참여자 ID")
    name: str = Field(..., description="참여자 이름")

    model_config = ConfigDict(from_attributes=True)

class ScheduleCreateRequest(BaseModel):
    name: str = Field(..., description="일정(회의)의 이름")
    start_time: datetime = Field(..., description="회의실 이용 시작 시간")
    end_time: datetime = Field(..., description="회의실 이용 종료 시간")
    room_id: int = Field(..., description="회의실 고유 번호")

    participants: list[int] = Field(..., min_length=1, description="일정에 참여할 참여자 ID 목록")


class ScheduleCreateResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime
    room_id: int

    model_config = ConfigDict(from_attributes=True)


class ScheduleDetailResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime
    room: RoomInfo
    participants: list[ParticipantInfo]

    model_config = ConfigDict(from_attributes=True)

class ScheduleUpdateRequest(BaseModel):
    name: str | None = Field(None, description="수정하려는 일정(회의)의 이름")
    start_time: datetime | None = Field(None, description="수정하려는 시작 시간")
    end_time: datetime | None = Field(None, description="수정하려는 종료 시간")
    room_id: int | None = Field(None, description="수정하려는 회의실 번호")


class ParticipantAddRequest(BaseModel):
    user_ids: list[int] = Field(..., min_length=1, description="기존 일정에 추가하려는 참여자 ID 배열")


class ParticipantAddResponse(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: datetime
    room_id: int
    participants: list[ParticipantInfo]

    model_config = ConfigDict(from_attributes=True)

class ScheduleUpdateRequest(BaseModel):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    room_id: Optional[int] = None