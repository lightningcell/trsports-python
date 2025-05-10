from . import db
from .associations import sport_facility

class Facility(db.Model):
    __tablename__ = 'facility'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    title = db.Column(db.String(100), nullable=False)  # Tesis başlığı
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)  # Şehir referansı
    district_id = db.Column(db.Integer, db.ForeignKey('district.id'), nullable=False)  # İlçe referansı

    # İlişkiler
    city = db.relationship('City', back_populates='facilities')  # City ile 1:n
    district = db.relationship('District', back_populates='facilities')  # District ile 1:n
    sports = db.relationship('Sport', secondary=sport_facility, back_populates='facilities')  # Çoktan-çoğa sporlar
    sessions = db.relationship('TrainSession', back_populates='facility')  # Seans kayıtları 