from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base
from .associations import sport_facility

class Sport(Base):
    __tablename__ = 'sport'
    id = Column(Integer, primary_key=True)  # Birincil anahtar
    name = Column(String(50), nullable=False)  # Spor dalı adı

    # İlişkiler
    memberships = relationship('Membership', back_populates='sport')  # Üyelikler
    sessions = relationship('TrainSession', back_populates='sport')  # Seanslar
    facilities = relationship('Facility', secondary=sport_facility, back_populates='sports')  # Çoktan-çoğa tesisler