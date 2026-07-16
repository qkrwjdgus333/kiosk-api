from app.database import SessionLocal, engine, Base
from app.domain.room.model import Room
from app.domain.user.model import User


def seed_data():
    db = SessionLocal()
    try:
        if db.query(Room).first():
            print("데이터가 이미 존재합니다. 시딩을 중단합니다.")
            return

        rooms = [
            Room(name="A 회의실", capacity=5),
            Room(name="B 회의실", capacity=10),
            Room(name="C 회의실", capacity=20)
        ]
        db.add_all(rooms)

        users = [User(name=f"사용자 {i}") for i in range(1, 21)]
        db.add_all(users)

        db.commit()
        print("초기 데이터(회의실 3개, 사용자 20명) 생성 완료!")

    except Exception as e:
        db.rollback()
        print(f"데이터 생성 중 에러 발생: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_data()