from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class TrainSession(Base):
    __tablename__ = 'train_session'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    start_datetime = Column(DateTime, nullable=False)  # Başlangıç zamanı
    end_datetime = Column(DateTime, nullable=False)  # Bitiş zamanı
    facility_id = Column(Integer, ForeignKey('facility.id'), nullable=False)  # Tesis referansı
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Kullanıcı referansı
    sport_id = Column(Integer, ForeignKey('sport.id'), nullable=False)  # Spor dalı referansı

    # İlişkiler
    facility = relationship('Facility', back_populates='sessions')  # Tesis bilgisi
    user = relationship('User', back_populates='sessions')  # Kullanıcı bilgisi
    sport = relationship('Sport', back_populates='sessions')  # Spor dalı bilgisi