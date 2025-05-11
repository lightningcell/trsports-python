from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from .base import Base

class Shopbag(Base):
    __tablename__ = 'shopbag'
    id = Column(Integer, primary_key=True)  # Birincil anahtar

    # İlişkiler
    user = relationship('User', back_populates='shopbag', uselist=False)  # 1:1 kullanıcı
    memberships = relationship('Membership', back_populates='shopbag')  # İçindeki üyelikler