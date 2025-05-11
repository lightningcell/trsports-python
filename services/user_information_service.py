from models.user_information import UserInformation
from db_singleton import SQLAlchemySessionSingleton

class UserInformationService:
    @staticmethod
    def get_by_id(info_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(UserInformation).get(info_id)

    @staticmethod
    def create(user_id, has_sport_past, has_disability, address):
        session_db = SQLAlchemySessionSingleton.get_session()
        info = UserInformation(
            user_id=user_id,
            has_sport_past=has_sport_past,
            has_disability=has_disability,
            address=address
        )
        session_db.add(info)
        session_db.commit()
        return info
