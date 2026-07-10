class BusinessException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(self.message)

class InvalidTimeRangeException(BusinessException):
    def __init__(self, message: str = "시작 시간과 종료시간의 범위가 이상합니다."):
        super().__init__(status_code=400, code="ENDTIME_EARIER_STARTTIME", message=message)


class RoomCapacityExceededException(BusinessException):
    def __init__(self, message: str = "회의실 수용 인원보다 참여자의 수가 더 많습니다."):
        super().__init__(status_code=400, code="ROOM_CAPACITY_EXCEED", message=message)