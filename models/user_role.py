from . import db
from .associations import user_userrole

class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(50), nullable=False)  # Rol adı

    # Çoktan-çoğa ilişki
    users = db.relationship('User', secondary=user_userrole, back_populates='roles') 