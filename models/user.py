from . import db
from .associations import user_userrole

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(100), nullable=False)  # İsmi
    surname = db.Column(db.String(100), nullable=False)  # Soyismi
    phone_number = db.Column(db.String(20), nullable=True)  # Telefon numarası
    email_address = db.Column(db.String(120), unique=True, nullable=False)  # E-posta (benzersiz)
    password = db.Column(db.String(128), nullable=False)  # Hashlenmiş parola
    shopbag_id = db.Column(db.Integer, db.ForeignKey('shopbag.id'), unique=True)  # 1:1 Shopbag referansı

    # İlişkiler
    shopbag = db.relationship('Shopbag', back_populates='user', uselist=False)  # 1:1 ilişki
    information = db.relationship('UserInformation', back_populates='user', uselist=False)  # 1:1 kişisel bilgi
    roles = db.relationship('UserRole', secondary=user_userrole, back_populates='users')  # Çoktan-çoğa roller
    memberships = db.relationship('Membership', back_populates='user')  # Üyelikleri
    sessions = db.relationship('TrainSession', back_populates='user')  # Antrenman seansları 