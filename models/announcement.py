from . import db

class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)  # Birincil anahtar
    title = db.Column(db.String(200), nullable=False)  # Duyuru başlığı
    content = db.Column(db.Text, nullable=False)  # Duyuru içeriği 