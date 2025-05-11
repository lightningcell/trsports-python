from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Membership(Base):
    __tablename__ = 'membership'
    id = Column(Integer, primary_key=True)
    is_proceed = Column(Boolean, default=False)  # Üyelik durumu
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Kullanıcı referansı
    shopbag_id = Column(Integer, ForeignKey('shopbag.id'), nullable=False)  # Shopbag referansı
    sport_id = Column(Integer, ForeignKey('sport.id'), nullable=False)  # Spor dalı referansı
    facility_id = Column(Integer, ForeignKey('facility.id'), nullable=False)  # Tesis referansı

    # İlişkiler
    user = relationship('User', back_populates='memberships')  # Kullanıcı bilgisi
    shopbag = relationship('Shopbag', back_populates='memberships')  # Shopbag bilgisi
    sport = relationship('Sport', back_populates='memberships')  # Spor dalı bilgisi