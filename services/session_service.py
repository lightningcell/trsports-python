from db_singleton import SQLAlchemySessionSingleton
from models.train_session import TrainSession
from models.sport import Sport
from models.facility import Facility
from datetime import datetime, date, time

class SessionService:
    @staticmethod
    def get_by_id(session_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(TrainSession).get(session_id)
        finally:
            session_db.close()

    @staticmethod
    def get_today_sessions(user_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            today = date.today()
            start_dt = datetime.combine(today, time.min)
            end_dt = datetime.combine(today, time.max)
            sessions = session_db.query(TrainSession).filter(
                TrainSession.user_id == user_id,
                TrainSession.start_datetime >= start_dt,
                TrainSession.start_datetime <= end_dt
            ).all()
            result = []
            for s in sessions:
                result.append({
                    'sport_name': s.sport.name,
                    'facility_name': s.facility.title,
                    'start': s.start_datetime.strftime('%H:%M'),
                    'end': s.end_datetime.strftime('%H:%M')
                })
            return {'sessions': result}
        finally:
            session_db.close()

    @staticmethod
    def book_session(membership, start_dt, end_dt, user_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            session_entry = TrainSession(
                start_datetime=start_dt,
                end_datetime=end_dt,
                facility_id=membership.facility_id,
                sport_id=membership.sport_id,
                user_id=user_id
            )
            session_db.add(session_entry)
            session_db.commit()
            return True
        finally:
            session_db.close()
