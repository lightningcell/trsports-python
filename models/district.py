from . import db

class District(db.Model):
    __tablename__ = 'district'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(100), nullable=False)  # İlçe adı
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)  # Şehre referans

    # İlişkiler
    city = db.relationship('City', back_populates='districts')  # Şehir bilgisi
    facilities = db.relationship('Facility', back_populates='district')  # İlçedeki tesisler 