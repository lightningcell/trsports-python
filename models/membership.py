from . import db

class Membership(db.Model):
    __tablename__ = 'membership'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    is_proceed = db.Column(db.Boolean, default=False)  # Üyelik durumu
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Kullanıcı referansı
    shopbag_id = db.Column(db.Integer, db.ForeignKey('shopbag.id'), nullable=False)  # Shopbag referansı
    sport_id = db.Column(db.Integer, db.ForeignKey('sport.id'), nullable=False)  # Spor dalı referansı

    # İlişkiler
    user = db.relationship('User', back_populates='memberships')  # Kullanıcı bilgisi
    shopbag = db.relationship('Shopbag', back_populates='memberships')  # Shopbag bilgisi
    sport = db.relationship('Sport', back_populates='memberships')  # Spor dalı bilgisi 