from db_singleton import SQLAlchemySessionSingleton
from models.city import City
from models.district import District
import json
from app import create_app
app = create_app()

SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
session = SQLAlchemySessionSingleton.get_session()

with app.app_context():
    with open('data/city.json', encoding='utf-8') as f:
        cities_json = json.load(f)
    with open('data/district.json', encoding='utf-8') as f:
        districts_json = json.load(f)

    # Şehirler için: sadece 'data' anahtarındaki listeyi kullan
    cities = None
    for entry in cities_json:
        if isinstance(entry, dict) and entry.get('data') and isinstance(entry['data'], list):
            cities = entry['data']
            break
    if not cities:
        raise Exception('city.json içinde data anahtarı bulunamadı.')
    for c in cities:
        city = session.query(City).get(int(c['id'])) or City(id=int(c['id']))
        city.name = c['name']
        session.merge(city)
    session.commit()

    # İlçeler için: sadece 'data' anahtarındaki listeyi kullan
    districts = None
    for entry in districts_json:
        if isinstance(entry, dict) and entry.get('data') and isinstance(entry['data'], list):
            districts = entry['data']
            break
    if not districts:
        raise Exception('district.json içinde data anahtarı bulunamadı.')
    for d in districts:
        district = session.query(District).get(int(d['id'])) or District(id=int(d['id']))
        district.name = d['name']
        district.city_id = int(d['il_id'])
        session.merge(district)
    session.commit()