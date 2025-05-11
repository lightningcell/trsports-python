from db_singleton import SQLAlchemySessionSingleton
from models.shopbag import Shopbag
from models.membership import Membership
from models.sport import Sport
from models.facility import Facility
from models.associations import sport_facility
from sqlalchemy import select, literal_column

class ShopbagService:
    @staticmethod
    def get_by_id(shopbag_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(Shopbag).get(shopbag_id)
        finally:
            session_db.close()

    @staticmethod
    def get_shopbag(user):
        if not user or not user.shopbag:
            return {'memberships': []}
        memberships = [
            {'id': m.id, 'sport_id': m.sport_id, 'facility_id': m.sport.facilities[0].id if m.sport.facilities else None}
            for m in user.shopbag.memberships
        ]
        return {'memberships': memberships}

    @staticmethod
    def add_membership(user, facility_id, sport_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if not user.shopbag:
                user.shopbag = Shopbag()
                session_db.merge(user.shopbag)  # Use merge to avoid session conflict
                session_db.commit()
            exists = session_db.query(Membership).filter_by(shopbag_id=user.shopbag.id, sport_id=sport_id).first()
            if exists:
                return {'error': 'Bu spor dalı zaten sepette.'}, 400
            membership = Membership(user_id=user.id, shopbag_id=user.shopbag.id, sport_id=sport_id, facility_id=facility_id)
            session_db.add(membership)
            session_db.commit()
            return {'success': True}
        finally:
            session_db.close()

    @staticmethod
    def count(user):
        if not user or not user.shopbag:
            return 0
        return len(user.shopbag.memberships)

    @staticmethod
    def detail(user):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if not user or not user.shopbag:
                return {
                    'memberships': [],
                    'total': 0,
                    'discounted_total': 0,
                    'is_student': False
                }
            is_student = any(role.name == 'Student' for role in user.roles)
            memberships = []
            total = 0
            for m in user.shopbag.memberships:
                sport = m.sport
                facility = None
                price = 0
                for f in sport.facilities:
                    if f.id == m.facility_id:
                        facility = f
                        price = session_db.execute(
                            select(literal_column('price')).select_from(sport_facility).where(
                                sport_facility.c.facility_id==f.id,
                                sport_facility.c.sport_id==sport.id
                            )
                        ).scalar() or 0
                        break
                memberships.append({
                    'id': m.id,
                    'sport_name': sport.name,
                    'facility_name': facility.title if facility else '',
                    'price': float(price)
                })
                total += float(price)
            discount = 0.5 if is_student else 1.0
            return {
                'memberships': memberships,
                'total': total,
                'discounted_total': total * discount,
                'is_student': is_student
            }
        finally:
            session_db.close()

    @staticmethod
    def clear(user):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if user and user.shopbag:
                for m in list(user.shopbag.memberships):
                    session_db.delete(m)
                session_db.commit()
            return {'success': True}
        finally:
            session_db.close()

    @staticmethod
    def remove_membership(user, membership_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            m = session_db.query(Membership).get(membership_id)
            if not m or m.user_id != user.id:
                return {'error': 'Yetkisiz veya bulunamadı'}, 403
            session_db.delete(m)
            session_db.commit()
            return {'success': True}
        finally:
            session_db.close()

    @staticmethod
    def proceed_payment(user):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            for m in list(user.shopbag.memberships):
                m.is_proceed = True
                m.shopbag_id = None
            session_db.commit()
            return True
        finally:
            session_db.close()
