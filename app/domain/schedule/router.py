from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session


from app.database import get_db
from app.domain.schedule.schema import *
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

@router.patch("/{id}", response_model=ScheduleDetailResponse, status_code=status.HTTP_200_OK)
def update_schedule(
    request: ScheduleUpdateRequest,
    id: int = Path(...),
    db: Session = Depends(get_db)
):
    
    try:
        return service.update_schedule(db=db, schedule_id=id, request=request)
    except BusinessException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail={"code": e.code, "message": e.message}
        )