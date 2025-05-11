from db_singleton import SQLAlchemySessionSingleton
from models.user import User
from models.user_role import UserRole
from werkzeug.security import generate_password_hash

# Veritabanı bağlantısını başlat
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
session = SQLAlchemySessionSingleton.get_session()

admin_role = session.query(UserRole).filter_by(name="Admin").first()
if not admin_role:
    raise Exception("Önce rolleri ekleyin.")
if not session.query(User).filter_by(name="MxAdmin").first():
    user = User(
        name="MxAdmin",
        surname="Admin",
        phone_number="",
        email_address="mxadmin@example.com",
        password=generate_password_hash("1")
    )
    user.roles.append(admin_role)
    session.add(user)
    session.commit()
    print("Admin kullanıcı eklendi.")
else:
    print("Admin kullanıcı zaten mevcut.")
