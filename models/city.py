from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class City(Base):
    __tablename__ = 'city'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    name = Column(String(100), nullable=False)  # Şehir adı

    # İlişkiler
    districts = relationship('District', back_populates='city')  # İlçeleri
    facilities = relationship('Facility', back_populates='city')  # Tesisleri