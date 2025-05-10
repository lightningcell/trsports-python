from . import db

class UserInformation(db.Model):
    __tablename__ = 'user_information'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)  # 1:1 Kullanıcı referansı
    has_sport_past = db.Column(db.Boolean, default=False)  # Spor geçmişi var mı?
    has_disability = db.Column(db.Boolean, default=False)  # Engelli mi?
    address = db.Column(db.String(255), nullable=True)  # Adres bilgisi

    # İlişkiler
    user = db.relationship('User', back_populates='information', uselist=False)  # Kullanıcı bilgisi 