from db_singleton import SQLAlchemySessionSingleton
from models.announcement import Announcement
from sqlalchemy import select

class AnnouncementService:
    @staticmethod
    def get_all():
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            notes = session_db.query(Announcement).all()
            return [{'id': n.id, 'title': n.title, 'content': n.content} for n in notes]
        finally:
            session_db.close()

    @staticmethod
    def get_by_id(announcement_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            return session_db.query(Announcement).get(announcement_id)
        finally:
            session_db.close()

    @staticmethod
    def create(title, content):
        session_db = SQLAlchemySessionSingleton.get_session()
        try:
            if not title or not content:
                return {'error': 'Başlık ve içerik gerekli.'}, 400
            note = Announcement(title=title, content=content)
            session_db.add(note)
            session_db.commit()
            return {'id': note.id, 'title': note.title, 'content': note.content}, 201
        finally:
            session_db.close()
