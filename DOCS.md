# TRSPORTS Projesi Geliştirici Dökümantasyonu

## İçindekiler
- [Genel Mimari ve Katmanlar](#genel-mimari-ve-katmanlar)
- [Singleton Tasarım Deseni](#singleton-tasarım-deseni)
- [Facade (Servis) Katmanı](#facade-servis-katmanı)
- [Veritabanı ve Modeller](#veritabanı-ve-modeller)
- [Servisler (Business Logic)](#servisler-business-logic)
- [Flask Uygulama Akışı ve Rotalar](#flask-uygulama-akışı-ve-rotalar)
- [Template ve Statik Dosya Yapısı](#template-ve-statik-dosya-yapısı)
- [Scriptler ve Yardımcı Araçlar](#scriptler-ve-yardımcı-araçlar)
- [Geliştiriciye Notlar ve En İyi Pratikler](#geliştiriciye-notlar-ve-en-iyi-pratikler)

---

## Genel Mimari ve Katmanlar

Proje, modern ve sürdürülebilir bir Python/Flask mimarisiyle geliştirilmiştir. Temel katmanlar şunlardır:
- **Flask Uygulama Katmanı:** HTTP endpoint'leri ve sayfa yönlendirmeleri.
- **Service (Facade) Katmanı:** Tüm iş mantığı ve veri erişimi burada kapsüllenmiştir.
- **Model Katmanı:** SQLAlchemy ile tanımlanmış veritabanı modelleri.
- **Singleton DB Yönetimi:** Tüm uygulama için tekil veritabanı bağlantısı ve session yönetimi.
- **Template ve Statik Dosyalar:** Kullanıcı arayüzü ve stiller.

## Singleton Tasarım Deseni

Veritabanı işlemleri için `db_singleton.py` dosyasındaki `SQLAlchemySessionSingleton` sınıfı kullanılır. Bu yapı sayesinde uygulama boyunca tek bir veritabanı bağlantısı ve session yönetimi sağlanır. Flask-SQLAlchemy yerine doğrudan SQLAlchemy ile çalışılır.

**Kullanım:**
```python
from db_singleton import SQLAlchemySessionSingleton
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
session = SQLAlchemySessionSingleton.get_session()
```
- `initialize` sadece bir kez çağrılır.
- Her işlemde yeni bir session alınabilir.
- Flask'ın kendi `session` objesi ile isim çakışmasına dikkat edin (genellikle `session_db` kullanılır).

Avantajları:
- Tek noktadan veritabanı yönetimi
- Kod tekrarını azaltır
- Test ve bakım kolaylığı sağlar

## Facade (Servis) Katmanı

Tüm iş mantığı ve veri erişimi, servis katmanında (ör. `services/` klasörü) kapsüllenmiştir. Route'lar doğrudan model ile değil, ilgili servis fonksiyonları ile iletişim kurar. Böylece kodun okunabilirliği ve sürdürülebilirliği artar.

**Başlıca Servisler:**
- `SportService`, `FacilityService`, `AnnouncementService`, `ShopbagService`, `MembershipService`, `SessionService`, `LocationService`

**Örnek Akış:**
```
Kullanıcı → Flask Route → Service (Facade) → Model/DB
```

**Koddan Örnek:**
```python
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
```

## Veritabanı ve Modeller

Tüm modeller `models/` klasöründe SQLAlchemy ile tanımlanmıştır. Temel modeller:
- **User, UserRole, UserInformation:** Kullanıcı ve rol yönetimi
- **Shopbag, Membership:** Sepet ve üyelik işlemleri
- **Facility, Sport, TrainSession:** Tesis, spor dalı ve seans yönetimi
- **City, District:** Lokasyon yönetimi
- **Announcement:** Duyurular
- **Ara Tablolar:** `user_userrole`, `sport_facility` (Çoktan-çoğa ilişkiler için)

Her modelde ilişkiler açıkça tanımlanmıştır. Örneğin, bir kullanıcının birden fazla rolü olabilir (`User.roles`), bir tesisin birden fazla spor dalı olabilir (`Facility.sports`).

## Servisler (Business Logic)

Her iş mantığı için ayrı bir servis sınıfı vardır. Servisler, doğrudan veritabanı işlemlerini ve iş kurallarını kapsar. Örneğin:
- `FacilityService.create(title, district_id, city_id)` yeni tesis ekler.
- `ShopbagService.add_membership(user, facility_id, sport_id)` kullanıcıya üyelik ekler.
- `SessionService.get_today_sessions(user_id)` kullanıcının bugünkü seanslarını listeler.

Servisler, Flask'a özgü nesnelerle (request, response) ilgilenmez, sadece iş mantığına odaklanır.

## Flask Uygulama Akışı ve Rotalar

Tüm HTTP endpoint'leri ve sayfa yönlendirmeleri `app.py` dosyasında tanımlıdır. Örnekler:
- `/register`, `/login`, `/logout`: Kullanıcı işlemleri
- `/api/sports`, `/api/facilities`, `/api/announcements`: API endpoint'leri
- `/shopbag`, `/shopbag/pay`: Sepet ve ödeme işlemleri
- `/membership/<int:membership_id>/sessions`: Seans seçimi

Her route, ilgili servis fonksiyonunu çağırır ve sonucu döner.

## Template ve Statik Dosya Yapısı

- **templates/**: Tüm HTML şablonları (Jinja2). Ana şablon `base.html`dir. Diğer sayfalar bunu genişletir.
  - `components/`: Tekrar kullanılabilir parça şablonlar (örn. navbar, popup).
- **static/css/**: Tüm stiller (CSS).
- **static/js/**: JavaScript dosyaları (örn. popup.js).
- **static/images/**: Görseller.

Kullanıcı arayüzü modern ve responsive olarak tasarlanmıştır. Tüm formlar, popup'lar ve dashboard bölümleri component tabanlıdır.

## Scriptler ve Yardımcı Araçlar

- `create_roles.py`, `create_admin.py`: Başlangıç rolleri ve admin kullanıcı oluşturmak için scriptler.
- `sync_city_and_district_with_db.py`: Şehir ve ilçe verilerini veritabanına senkronize eder.

## Geliştiriciye Notlar ve En İyi Pratikler

- Kodun tamamı PEP8 standartlarına uygun yazılmıştır.
- Her yeni işlev için önce servis katmanına fonksiyon ekleyin, ardından route'u oluşturun.
- Model ilişkilerini ve migration işlemlerini dikkatli yönetin.
- Singleton DB yönetimi dışında Flask-SQLAlchemy kullanılmaz.
- Test ve bakım kolaylığı için iş mantığını servislerde tutun.
- UI/UX için component ve template yapısını bozmadan geliştirme yapın.

---

Herhangi bir sorunda veya mimariyle ilgili kararsızlıkta, `FACADE.md` ve `SINGLETON.md` dosyalarını inceleyin. Kodun sürdürülebilirliği için bu mimari prensiplere sadık kalın.
