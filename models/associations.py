from . import db

# Ara tablolar (Many-to-Many ilişkiler)

# Kullanıcılar ile Roller arasındaki çoktan çoğa ilişki
user_userrole = db.Table(
    'user_userrole',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('user_role_id', db.Integer, db.ForeignKey('user_role.id'), primary_key=True)
)

# Tesisler ile Spor dalları arasındaki çoktan çoğa ilişki
sport_facility = db.Table(
    'sport_facility',
    db.Column('facility_id', db.Integer, db.ForeignKey('facility.id'), primary_key=True),
    db.Column('sport_id', db.Integer, db.ForeignKey('sport.id'), primary_key=True)
) 