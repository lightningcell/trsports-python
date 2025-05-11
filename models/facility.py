from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .associations import sport_facility

class Facility(Base):
    __tablename__ = 'facility'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    title = Column(String(100), nullable=False)  # Tesis başlığı
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)  # Şehir referansı
    district_id = Column(Integer, ForeignKey('district.id'), nullable=False)  # İlçe referansı

    # İlişkiler
    city = relationship('City', back_populates='facilities')  # City ile 1:n
    district = relationship('District', back_populates='facilities')  # District ile 1:n
    sports = relationship('Sport', secondary=sport_facility, back_populates='facilities')  # Çoktan-çoğa sporlar
    sessions = relationship('TrainSession', back_populates='facility')  # Seans kayıtları