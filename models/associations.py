from sqlalchemy import Table, Column, Integer, ForeignKey, Numeric
from .base import Base

# Ara tablolar (Many-to-Many ilişkiler)

# Kullanıcılar ile Roller arasındaki çoktan çoğa ilişki
user_userrole = Table(
    'user_userrole',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('user_role_id', Integer, ForeignKey('user_role.id'), primary_key=True)
)

# Tesisler ile Spor dalları arasındaki çoktan çoğa ilişki
sport_facility = Table(
    'sport_facility',
    Base.metadata,
    Column('facility_id', Integer, ForeignKey('facility.id'), primary_key=True),
    Column('sport_id', Integer, ForeignKey('sport.id'), primary_key=True),
    Column('price', Numeric(10, 2), nullable=False, default=0)
)