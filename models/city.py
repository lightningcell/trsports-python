from . import db

class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    name = db.Column(db.String(100), nullable=False)  # Şehir adı

    # İlişkiler
    districts = db.relationship('District', back_populates='city')  # İlçeleri
    facilities = db.relationship('Facility', back_populates='city')  # Tesisleri 