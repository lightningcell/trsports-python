from db_singleton import SQLAlchemySessionSingleton
from models.membership import Membership
from models.sport import Sport
from models.facility import Facility
from models.associations import sport_facility
from sqlalchemy import select, literal_column
from models.train_session import TrainSession
from datetime import datetime, date, time, timedelta
from flask import render_template

class MembershipService:
    @staticmethod
    def get_by_id(membership_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(Membership).get(membership_id)
        finally:
            session_db.close()

    @staticmethod
    def get_proceed_memberships(user):
        # user zaten session_db'den geldiği için burada close gerekmiyor
        memberships = []
        for m in user.memberships:
            if getattr(m, 'is_proceed', False):
                sport = m.sport
                facility = None
                for f in sport.facilities:
                    if f.id == m.facility_id:
                        facility = f
                        break
                memberships.append({
                    'id': m.id,
                    'sport_name': sport.name,
                    'facility_name': facility.title if facility else ''
                })
        return {'memberships': memberships}

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

    @staticmethod
    def get_sessions(membership_id, user_id):
        session = SQLAlchemySessionSingleton.get_session()
        try:
            m = session.query(Membership).get(membership_id)
            if m.user_id != user_id or not m.is_proceed:
                return None
            facility = session.query(Facility).get(m.facility_id)
            sport = session.query(Sport).get(m.sport_id)
            return facility, sport
        finally:
            session.close()

    @staticmethod
    def get_membership_session_page(membership_id, user_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            m = session_db.query(Membership).get(membership_id)
            if not m or m.user_id != user_id or not m.is_proceed:
                return None, None, None, None
            facility = session_db.query(Facility).get(m.facility_id)
            sport = session_db.query(Sport).get(m.sport_id)
            today = date.today()
            weekday = today.weekday()  # Monday=0
            week_dates = [(today + timedelta(days=(i-weekday))).strftime('%Y-%m-%d') for i in range(7)]
            return facility, sport, membership_id, week_dates
        finally:
            session_db.close()

    @staticmethod
    def book_session(membership_id, user_id, start_str, end_str, date_str):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            m = session_db.query(Membership).get(membership_id)
            if not m or m.user_id != user_id or not m.is_proceed:
                return False
            if not date_str or date_str.lower() == 'null':
                selected_date = date.today()
            else:
                try:
                    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                except ValueError:
                    selected_date = date.today()
            try:
                sh, sm = map(int, start_str.split(':'))
                eh, em = map(int, end_str.split(':'))
                start_dt = datetime.combine(selected_date, time(sh, sm))
                end_dt = datetime.combine(selected_date, time(eh, em))
            except:
                return False
            session_entry = TrainSession(
                start_datetime=start_dt,
                end_datetime=end_dt,
                facility_id=m.facility_id,
                sport_id=m.sport_id,
                user_id=user_id
            )
            session_db.add(session_entry)
            session_db.commit()
            return True
        finally:
            session_db.close()

class MembershipSessionService:
    @staticmethod
    def get_membership_session_page(membership_id, user_id):
        session = SQLAlchemySessionSingleton.get_session()
        m = session.query(Membership).get(membership_id)
        if m.user_id != user_id or not m.is_proceed:
            return None, None, None, None
        facility = session.query(Facility).get(m.facility_id)
        sport = session.query(Sport).get(m.sport_id)
        today = date.today()
        weekday = today.weekday()  # Monday=0
        week_dates = [(today + timedelta(days=(i-weekday))).strftime('%Y-%m-%d') for i in range(7)]
        return facility, sport, membership_id, week_dates

    @staticmethod
    def book_session(membership_id, user_id, start_str, end_str, date_str):
        session = SQLAlchemySessionSingleton.get_session()
        m = session.query(Membership).get(membership_id)
        if m.user_id != user_id or not m.is_proceed:
            return False
        if not date_str or date_str.lower() == 'null':
            selected_date = date.today()
        else:
            try:
                selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                selected_date = date.today()
        try:
            sh, sm = map(int, start_str.split(':'))
            eh, em = map(int, end_str.split(':'))
            start_dt = datetime.combine(selected_date, time(sh, sm))
            end_dt = datetime.combine(selected_date, time(eh, em))
        except:
            return False
        session_entry = TrainSession(
            start_datetime=start_dt,
            end_datetime=end_dt,
            facility_id=m.facility_id,
            sport_id=m.sport_id,
            user_id=user_id
        )
        session.add(session_entry)
        session.commit()
        return True
