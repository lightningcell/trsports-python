from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class District(Base):
    __tablename__ = 'district'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    name = Column(String(100), nullable=False)  # İlçe adı
    city_id = Column(Integer, ForeignKey('city.id'), nullable=False)  # Şehre referans

    # İlişkiler
    city = relationship('City', back_populates='districts')  # Şehir bilgisi
    facilities = relationship('Facility', back_populates='district')  # İlçedeki tesisler