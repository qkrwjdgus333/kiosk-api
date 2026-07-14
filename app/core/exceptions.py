class BusinessException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(self.message)

class InvalidTimeRangeException(BusinessException):
    def __init__(self, message: str = "시작 시간과 종료시간의 범위가 이상합니다."):
        super().__init__(status_code=400, code="ENDTIME_EARIER_STARTTIME", message=message)


class RoomNotFoundException(BusinessException):
    def __init__(self, message: str = "유효하지 않은 회의실을 입력했습니다."):
        super().__init__(status_code=404, code="INVALID_ROOM_ID", message=message)

class RoomCapacityExceededException(BusinessException):
    def __init__(self, message: str = "회의실 수용 인원보다 참여자의 수가 더 많습니다."):
        super().__init__(status_code=400, code="ROOM_CAPACITY_EXCEED", message=message)

class UserNotFoundException(BusinessException):
    def __init__(self, message: str = "존재하지 않는 참여자를 입력했습니다."):
        super().__init__(status_code=404, code="USER_NOT_FOUND", message=message)

class ScheduleConflictException(BusinessException):
    def __init__(self, message: str = "신청하신 회의실이 이미 예약이 되어있습니다."):
        super().__init__(status_code=409, code="CONFLICT_RESERVATION_ROOM", message=message)


class ParticipantConflictException(BusinessException):
    def __init__(self, message: str = "초대한 참여자가 다른 회의에 이미 참여중입니다."):
        super().__init__(status_code=409, code="RESERVATION_CONFLICT_PARTICIPANTS", message=message)



class ScheduleNotFoundException(BusinessException):
    def __init__(self, message: str = "존재하지 않는 회의를 입력했습니다."):
        super().__init__(status_code=404, code="INVALID_SCHEDULES_ID", message=message)