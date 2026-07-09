from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from app.database import Base, engine


class Participant(Base):
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    schedule_id = Column(Integer, ForeignKey('schedule.id'))
    name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)

Base.metadata.create_all(engine)