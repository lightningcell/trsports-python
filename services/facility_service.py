from db_singleton import SQLAlchemySessionSingleton
from models.facility import Facility
from models.district import District
from models.city import City
from models.associations import sport_facility
from models.sport import Sport
from sqlalchemy import select, literal_column

class FacilityService:
    @staticmethod
    def get_all():
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            facilities = session_db.query(Facility).join(District).join(City).all()
            result = []
            for f in facilities:
                result.append({
                    'id': f.id,
                    'name': f.title,
                    'district': f.district.name,
                    'city': f.city.name
                })
            return result
        finally:
            session_db.close()

    @staticmethod
    def get_by_id(facility_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(Facility).get(facility_id)
        finally:
            session_db.close()

    @staticmethod
    def create(title, district_id, city_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if not title or not district_id or not city_id:
                return {'error': 'Başlık, il ve ilçe gerekli.'}, 400
            if session_db.query(Facility).filter_by(title=title).first():
                return {'error': 'Bu isimde tesis zaten var.'}, 400
            f = Facility(title=title, district_id=district_id, city_id=city_id)
            session_db.add(f)
            session_db.commit()
            return {'id': f.id, 'name': f.title}, 201
        finally:
            session_db.close()

    @staticmethod
    def add_sport(facility_id, sport_id, price):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if sport_id is None or price is None:
                return {'error': 'sport_id ve price gerekli.'}, 400
            try:
                price = float(price)
            except:
                return {'error': 'Geçersiz fiyat.'}, 400
            if price < 0:
                return {'error': 'Fiyat negatif olamaz.'}, 400
            facility = session_db.query(Facility).get(facility_id)
            exists = session_db.execute(
                select(sport_facility).where(
                    sport_facility.c.facility_id==facility_id,
                    sport_facility.c.sport_id==sport_id
                )
            ).first()
            if exists:
                return {'error': 'Bu spor zaten ekli.'}, 400
            session_db.execute(
                sport_facility.insert().values(
                    facility_id=facility_id,
                    sport_id=sport_id,
                    price=price
                )
            )
            session_db.commit()
            return {'success': True}, 201
        finally:
            session_db.close()

    @staticmethod
    def get_facility_sports(facility_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            stmt = select(
                Sport.id,
                Sport.name,
                literal_column('sport_facility.price').label('price')
            ).select_from(Sport.__table__.join(sport_facility, Sport.id==sport_facility.c.sport_id)).where(sport_facility.c.facility_id==facility_id)
            result = session_db.execute(stmt).all()
            return [{'id': row.id, 'name': row.name, 'price': float(row.price)} for row in result]
        finally:
            session_db.close()

    @staticmethod
    def remove_sport(facility_id, sport_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            facility = session_db.query(Facility).get(facility_id)
            sport = session_db.query(Sport).get(sport_id)
            if sport not in facility.sports:
                return {'error': 'Bu spor tesiste yok.'}, 400
            facility.sports.remove(sport)
            session_db.commit()
            return {'success': True}
        finally:
            session_db.close()
