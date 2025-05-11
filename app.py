from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.user_information import UserInformation
from models.user_role import UserRole
from models.sport import Sport
from models.facility import Facility
from models.district import District
from models.city import City
from models.announcement import Announcement
from models.associations import sport_facility
from sqlalchemy import select, literal_column
from datetime import datetime, date, time, timedelta
from models.train_session import TrainSession
from services.sport_service import SportService
from services.facility_service import FacilityService
from services.announcement_service import AnnouncementService
from services.shopbag_service import ShopbagService
from services.membership_service import MembershipService
from services.session_service import SessionService
from services.location_service import LocationService
from db_singleton import SQLAlchemySessionSingleton


def create_app():
    app = Flask(__name__)
    # Uygulama yapılandırması
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trsports.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'your-secret-key'
    # Medya yükleme dizini
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'media', 'uploads')

    # SQLAlchemy Singleton başlat
    SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')

    # Veritabanı tablolarını oluştur (ilk çalışma için)
    from models.base import Base
    engine = SQLAlchemySessionSingleton._engine
    with app.app_context():
        Base.metadata.create_all(bind=engine)


    # ----- Rotalar -----
    @app.route('/')
    def home():
        if 'user_id' not in session:
            return render_template('index.html')
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        if user and any(role.name == 'Admin' for role in user.roles):
            return render_template('admin_home.html')
        # User rolü için ana sayfa user_home.html
        return render_template('user_home.html')

    @app.route('/announcements')
    def announcements():
        return render_template('announcements.html')

    @app.route('/packages')
    def packages():
        return render_template('packages.html')

    @app.route('/sports')
    def sports():
        return render_template('sports.html')

    @app.route('/student-apply')
    def student_apply():
        return render_template('student_apply.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            name = request.form.get('first_name')
            surname = request.form.get('surname', '')
            phone = request.form.get('phone')
            email = request.form.get('email')
            password = request.form.get('password')
            password2 = request.form.get('password2')
            is_student = request.form.get('is_student') == 'on'
            if not name or not email or not password or not password2:
                return render_template('register.html', error="Tüm zorunlu alanları doldurun.")
            if password != password2:
                return render_template('register.html', error="Şifreler eşleşmiyor.")
            session_db = SQLAlchemySessionSingleton.get_session()
            if session_db.query(User).filter_by(email_address=email).first():
                return render_template('register.html', error="Bu email ile kayıtlı kullanıcı var.")
            user_role = session_db.query(UserRole).filter_by(name="User").first()
            student_role = session_db.query(UserRole).filter_by(name="Student").first() if is_student else None
            user = User(
                name=name,
                surname=surname,
                phone_number=phone,
                email_address=email,
                password=generate_password_hash(password)
            )
            if user_role:
                user.roles.append(user_role)
            if student_role:
                user.roles.append(student_role)
            session_db.add(user)
            session_db.commit()
            info = UserInformation(
                user_id=user.id,
                has_sport_past=request.form.get('sports_history') == 'yes',
                has_disability=request.form.get('disability') == 'yes',
                address=request.form.get('address', '')
            )
            session_db.add(info)
            session_db.commit()
            return redirect(url_for('login'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = None
            session_db = SQLAlchemySessionSingleton.get_session()
            # Kullanıcı adı veya email ile giriş
            if username:
                user = session_db.query(User).filter((User.name == username) | (User.email_address == username)).first()
            if not user or not check_password_hash(user.password, password):
                return render_template('login.html', error="Kullanıcı adı/email veya şifre hatalı.")
            # Giriş başarılı, session'a kullanıcıyı al
            session['user_id'] = user.id
            session['user_name'] = user.name
            return redirect(url_for('home'))
        return render_template('login.html')


    # OAuth login route for social authentication
    @app.route('/oauth_login/<provider>')
    def oauth_login(provider):
        # TODO: implement OAuth logic for providers like Google and Microsoft
        return redirect(url_for('home'))

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login'))

    @app.route('/popup/sport_create')
    def popup_sport_create():
        return render_template('components/popup_sport_create.html')

    @app.route('/api/sports', methods=['GET'])
    def api_get_sports():
        return jsonify(SportService.get_all())

    @app.route('/api/sports', methods=['POST'])
    def api_create_sport():
        data = request.get_json()
        name = data.get('name', '').strip()
        result = SportService.create(name)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/cities', methods=['GET'])
    def api_get_cities():
        return jsonify(LocationService.get_cities())

    @app.route('/api/districts', methods=['GET'])
    def api_get_districts():
        city_id = request.args.get('city_id', type=int)
        return jsonify(LocationService.get_districts(city_id))

    @app.route('/api/facilities', methods=['GET'])
    def api_get_facilities():
        return jsonify(FacilityService.get_all())

    @app.route('/api/facilities', methods=['POST'])
    def api_create_facility():
        data = request.get_json()
        title = data.get('name', '').strip()
        district_id = data.get('district_id')
        city_id = data.get('city_id')
        result = FacilityService.create(title, district_id, city_id)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/announcements', methods=['GET'])
    def api_get_announcements():
        return jsonify(AnnouncementService.get_all())

    @app.route('/api/announcements', methods=['POST'])
    def api_create_announcement():
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        result = AnnouncementService.create(title, content)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/facilities/by_location')
    def api_facilities_by_location():
        city_id = request.args.get('city_id', type=int)
        district_id = request.args.get('district_id', type=int)
        return jsonify(LocationService.get_facilities_by_location(city_id, district_id))

    @app.route('/api/shopbag')
    def api_get_shopbag():
        if 'user_id' not in session:
            return '', 401
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        return jsonify(ShopbagService.get_shopbag(user))

    @app.route('/api/shopbag/add_membership', methods=['POST'])
    def api_add_membership_to_shopbag():
        if 'user_id' not in session:
            return '', 401
        data = request.get_json()
        facility_id = data.get('facility_id')
        sport_id = data.get('sport_id')
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        result = ShopbagService.add_membership(user, facility_id, sport_id)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/shopbag/count')
    def api_shopbag_count():
        if 'user_id' not in session:
            return jsonify({'count': 0})
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        return jsonify({'count': ShopbagService.count(user)})

    @app.route('/api/shopbag/detail')
    def api_shopbag_detail():
        if 'user_id' not in session:
            return '', 401
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        return jsonify(ShopbagService.detail(user))

    @app.route('/api/shopbag/clear', methods=['POST'])
    def api_shopbag_clear():
        if 'user_id' not in session:
            return '', 401
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        return jsonify(ShopbagService.clear(user))

    @app.route('/api/shopbag/remove_membership/<int:membership_id>', methods=['POST'])
    def api_remove_membership_from_shopbag(membership_id):
        if 'user_id' not in session:
            return '', 401
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        result = ShopbagService.remove_membership(user, membership_id)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/memberships/proceed')
    def api_get_proceed_memberships():
        if 'user_id' not in session:
            return '', 401
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        return jsonify(MembershipService.get_proceed_memberships(user))

    @app.route('/api/sessions/today')
    def api_get_today_sessions():
        if 'user_id' not in session:
            return '', 401
        return jsonify(SessionService.get_today_sessions(session['user_id']))

    @app.route('/popup/facility_create')
    def popup_facility_create():
        return render_template('components/popup_facility_create.html')

    @app.route('/popup/announcement_create')
    def popup_announcement_create():
        return render_template('components/popup_announcement_create.html')

    @app.route('/popup/facility_sport_add')
    def popup_facility_sport_add():
        return render_template('components/popup_facility_sport_add.html')

    @app.route('/facility/<int:facility_id>/sports', methods=['GET'])
    def facility_sports_page(facility_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        facility = session_db.query(Facility).get(facility_id)
        # Tesisin sporları ve tüm sporlar
        all_sports = session_db.query(Sport).all()
        return render_template('facility_sports.html', facility=facility, all_sports=all_sports)

    @app.route('/api/facility/<int:facility_id>/sports', methods=['GET'])
    def api_get_facility_sports(facility_id):
        # return list with price
        stmt = select(
            Sport.id,
            Sport.name,
            literal_column('sport_facility.price').label('price')
        ).\
         select_from(Sport.__table__.join(sport_facility, Sport.id==sport_facility.c.sport_id)).\
         where(sport_facility.c.facility_id==facility_id)
        session_db = SQLAlchemySessionSingleton.get_session()
        result = session_db.execute(stmt).all()
        return jsonify([{'id': row.id, 'name': row.name, 'price': float(row.price)} for row in result])

    @app.route('/api/facility/<int:facility_id>/sports', methods=['POST'])
    def api_add_sport_to_facility(facility_id):
        data = request.get_json()
        sport_id = data.get('sport_id')
        price = data.get('price')
        result = FacilityService.add_sport(facility_id, sport_id, price)
        if isinstance(result, tuple):
            return jsonify(result[0]), result[1]
        return jsonify(result)

    @app.route('/api/facility/<int:facility_id>/sports/<int:sport_id>', methods=['DELETE'])
    def api_remove_sport_from_facility(facility_id, sport_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        facility = session_db.query(Facility).get(facility_id)
        sport = session_db.query(Sport).get(sport_id)
        if sport not in facility.sports:
            return jsonify({'error': 'Bu spor tesiste yok.'}), 400
        facility.sports.remove(sport)
        session_db.commit()
        return jsonify({'success': True})

    @app.route('/shopbag')
    def shopbag():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return render_template('shopbag.html')

    @app.route('/shopbag/pay', methods=['GET', 'POST'])
    def payment():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        session_db = SQLAlchemySessionSingleton.get_session()
        user = session_db.query(User).get(session['user_id'])
        if request.method == 'POST':
            # Shopbag'deki membership'lerin is_proceed alanını True yap ve shopbag bağlantısını kaldır
            for m in list(user.shopbag.memberships):
                m.is_proceed = True
                m.shopbag_id = None  # Sepet bağlantısını kaldır
            session_db.commit()
            return redirect(url_for('payment_success'))
        return render_template('payment.html')

    @app.route('/shopbag/payment_success')
    def payment_success():
        user_name = session.get('user_name', 'KULLANICI')
        return render_template('payment_success.html', user_name=user_name)

    @app.route('/membership/<int:membership_id>/sessions')
    def membership_sessions(membership_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        facility, sport, membership_id, week_dates = MembershipService.get_membership_session_page(membership_id, session['user_id'])
        if not facility:
            return '', 403
        return render_template('session_select.html', facility=facility, sport=sport, membership_id=membership_id, week_dates=week_dates)

    @app.route('/book_session')
    def book_session():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        membership_id = request.args.get('membership_id', type=int)
        start_str = request.args.get('start')
        end_str = request.args.get('end')
        date_str = request.args.get('date')
        success = MembershipService.book_session(membership_id, session['user_id'], start_str, end_str, date_str)
        if not success:
            return '', 400
        return redirect(url_for('home'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)