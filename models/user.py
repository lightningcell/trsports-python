from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .associations import user_userrole

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    name = Column(String(100), nullable=False)  # İsmi
    surname = Column(String(100), nullable=False)  # Soyismi
    phone_number = Column(String(20), nullable=True)  # Telefon numarası
    email_address = Column(String(120), unique=True, nullable=False)  # E-posta (benzersiz)
    password = Column(String(128), nullable=False)  # Hashlenmiş parola
    shopbag_id = Column(Integer, ForeignKey('shopbag.id'), unique=True)  # 1:1 Shopbag referansı

    # İlişkiler
    shopbag = relationship('Shopbag', back_populates='user', uselist=False)  # 1:1 ilişki
    information = relationship('UserInformation', back_populates='user', uselist=False)  # 1:1 kişisel bilgi
    roles = relationship('UserRole', secondary=user_userrole, back_populates='users')  # Çoktan-çoğa roller
    memberships = relationship('Membership', back_populates='user')  # Üyelikleri
    sessions = relationship('TrainSession', back_populates='user')  # Antrenman seansları