from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session


from app.database import get_db
from app.domain.schedule.schema import ScheduleCreateRequest, ScheduleCreateResponse, ScheduleDetailResponse
from app.domain.schedule import service
from app.core.exceptions import BusinessException

router = APIRouter(prefix="/schedule", tags=["Schedule"])

@router.post("", response_model=ScheduleCreateResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(request: ScheduleCreateRequest, db: Session = Depends(get_db)) :
    try:
        new_schedule = service.create_schedule(db, request)
        return new_schedule
    except BusinessException as e:
        raise HTTPException(status_code=e.status_code, detail={"code": e.code, "message": e.message})
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": "DOMAIN_VALIDATION_ERROR", "message": str(e)}
        )

def get_schedule(id: int = Path(..., description="조회하려는 일정의 ID"),
                 db: Session = Depends(get_db)):
    try:
        return service.get_schedule(db, id)
    except BusinessException as e:
        raise HTTPException(status_code=e.status_code,
                            detail={"code": e.code, "message": e.message}
                            )