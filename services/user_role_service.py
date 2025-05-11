from models.user_role import UserRole
from db_singleton import SQLAlchemySessionSingleton

class UserRoleService:
    @staticmethod
    def get_by_id(role_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(UserRole).get(role_id)

    @staticmethod
    def get_by_name(name):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(UserRole).filter_by(name=name).first()
