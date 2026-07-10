from fastapi import FastAPI
from app.database import Base, engine

from app.domain.schedule.router import router as schedule_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="회의실 예약 키오스크 API",
    description="Python 3.13 + FastAPI 구현 과제",
    version="1.0.0"
)

app.include_router(schedule_router)

@app.get("/")
def health_check():
    return {"status": "ok"}