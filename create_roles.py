from db_singleton import SQLAlchemySessionSingleton
from models.user_role import UserRole

# Veritabanı bağlantısını başlat
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
session = SQLAlchemySessionSingleton.get_session()

for role_name in ["Admin", "User", "Student"]:
    if not session.query(UserRole).filter_by(name=role_name).first():
        session.add(UserRole(name=role_name))
session.commit()
print("Roller başarıyla eklendi.")
