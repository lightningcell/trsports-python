from . import db

class Shopbag(db.Model):
    __tablename__ = 'shopbag'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar

    # İlişkiler
    user = db.relationship('User', back_populates='shopbag', uselist=False)  # 1:1 kullanıcı
    memberships = db.relationship('Membership', back_populates='shopbag')  # İçindeki üyelikler 