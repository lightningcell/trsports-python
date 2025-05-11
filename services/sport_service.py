from db_singleton import SQLAlchemySessionSingleton
from models.sport import Sport
from sqlalchemy import select, literal_column

class SportService:
    @staticmethod
    def get_all():
        session_db = SQLAlchemySessionSingleton.get_session()
        sports = session_db.query(Sport).all()
        return [{'id': s.id, 'name': s.name} for s in sports]

    @staticmethod
    def get_by_id(sport_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(Sport).get(sport_id)

    @staticmethod
    def create(name):
        session_db = SQLAlchemySessionSingleton.get_session()
        if not name:
            return {'error': 'Spor adı zorunlu.'}, 400
        if session_db.query(Sport).filter_by(name=name).first():
            return {'error': 'Bu isimde bir spor zaten var.'}, 400
        sport = Sport(name=name)
        session_db.add(sport)
        session_db.commit()
        return {'id': sport.id, 'name': sport.name}, 201
