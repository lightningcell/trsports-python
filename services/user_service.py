from models.user import User
from db_singleton import SQLAlchemySessionSingleton
from werkzeug.security import generate_password_hash

class UserService:
    @staticmethod
    def get_by_id(user_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(User).get(user_id)

    @staticmethod
    def get_by_email(email):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(User).filter_by(email_address=email).first()

    @staticmethod
    def get_by_username_or_email(username):
        session_db = SQLAlchemySessionSingleton.get_session()
        return session_db.query(User).filter((User.name == username) | (User.email_address == username)).first()

    @staticmethod
    def create(name, surname, phone, email, password, user_role, student_role=None):
        session_db = SQLAlchemySessionSingleton.get_session()
        user = User(
            name=name,
            surname=surname,
            phone_number=phone,
            email_address=email,
            password=generate_password_hash(password)
        )
        if user_role:
            user.roles.append(user_role)
        if student_role:
            user.roles.append(student_role)
        session_db.add(user)
        session_db.commit()
        return user
