from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base

class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    users = relationship('User', secondary='user_userrole', back_populates='roles')