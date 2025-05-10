from . import db
from .associations import sport_facility

class Sport(db.Model):
    __tablename__ = 'sport'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(50), nullable=False)  # Spor dalı adı

    # İlişkiler
    memberships = db.relationship('Membership', back_populates='sport')  # Üyelikler
    sessions = db.relationship('TrainSession', back_populates='sport')  # Seanslar
    facilities = db.relationship('Facility', secondary=sport_facility, back_populates='sports')  # Çoktan-çoğa tesisler 