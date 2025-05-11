from sqlalchemy import Column, Integer, String, Text
from .base import Base

class Announcement(Base):
    __tablename__ = 'announcement'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # Duyuru başlığı
    content = Column(Text, nullable=False)  # Duyuru içeriği