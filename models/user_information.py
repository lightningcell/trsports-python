from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from .base import Base

class UserInformation(Base):
    __tablename__ = 'user_information'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), unique=True)  # 1:1 Kullanıcı referansı
    has_sport_past = Column(Boolean, default=False)  # Spor geçmişi var mı?
    has_disability = Column(Boolean, default=False)  # Engelli mi?
    address = Column(String(255), nullable=True)  # Adres bilgisi

    # İlişkiler
    user = relationship('User', back_populates='information', uselist=False)  # Kullanıcı bilgisi