from . import db

class TrainSession(db.Model):
    __tablename__ = 'train_session'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    start_datetime = db.Column(db.DateTime, nullable=False)  # Başlangıç zamanı
    end_datetime = db.Column(db.DateTime, nullable=False)  # Bitiş zamanı
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), nullable=False)  # Tesis referansı
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Kullanıcı referansı
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)  # Spor dalı referansı

    # İlişkiler
    facility = db.relationship('Facility', back_populates='sessions')  # Tesis bilgisi
    user = db.relationship('User', back_populates='sessions')  # Kullanıcı bilgisi
    sport = db.relationship('Sport', back_populates='sessions')  # Spor dalı bilgisi 