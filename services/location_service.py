from db_singleton import SQLAlchemySessionSingleton
from models.city import City
from models.district import District
from models.facility import Facility

class LocationService:
    @staticmethod
    def get_cities():
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            cities = session_db.query(City).all()
            return [{'id': c.id, 'name': c.name} for c in cities]
        finally:
            session_db.close()

    @staticmethod
    def get_by_id_city(city_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(City).get(city_id)
        finally:
            session_db.close()

    @staticmethod
    def get_districts(city_id=None):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            query = session_db.query(District)
            if city_id:
                query = query.filter_by(city_id=city_id)
            districts = query.all()
            return [{'id': d.id, 'name': d.name, 'city_id': d.city_id} for d in districts]
        finally:
            session_db.close()

    @staticmethod
    def get_by_id_district(district_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(District).get(district_id)
        finally:
            session_db.close()

    @staticmethod
    def get_facilities_by_location(city_id=None, district_id=None):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            q = session_db.query(Facility)
            if city_id:
                q = q.filter_by(city_id=city_id)
            if district_id:
                q = q.filter_by(district_id=district_id)
            facilities = q.all()
            return [{'id': f.id, 'name': f.title} for f in facilities]
        finally:
            session_db.close()
