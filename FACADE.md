# Facade (Yüzey) Tasarım Deseni Kullanımı Dökümantasyonu

## 1. Facade Deseni Nedir?
Facade (Yüzey) tasarım deseni, karmaşık alt sistemlerin işlevselliğini sadeleştirerek, üst katmanlara tek bir arayüz sunar. Böylece, sistemin karmaşıklığı gizlenir ve kullanım kolaylığı sağlanır. Facade, istemcinin alt sistemin detaylarını bilmeden işlemleri gerçekleştirmesine olanak tanır.

## 2. Projede Facade Deseni Nasıl Kullanıldı?
Bu projede Facade deseni, **service (servis) katmanı** ile uygulanmıştır. Flask uygulamasındaki route'lar (yani HTTP endpoint'leri), doğrudan model veya veritabanı işlemleriyle uğraşmak yerine, ilgili servis sınıflarını kullanır. Servisler, iş mantığı ve veri erişim katmanlarının karmaşıklığını gizleyerek, üst katmana sade ve tutarlı bir API sunar.

### Servis Katmanları (Facade)
- `SportService`
- `FacilityService`
- `AnnouncementService`
- `ShopbagService`
- `MembershipService`
- `SessionService`
- `LocationService`

Her bir servis, ilgili iş mantığını ve veri tabanı işlemlerini kapsüller. Route'lar ise sadece bu servislerin fonksiyonlarını çağırır.

## 3. Koddan Örnekler

### a) Route → Service → Model Akışı

Örnek: Yeni bir tesis ekleme

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

Burada, Flask route'u doğrudan model ile değil, `FacilityService.create` fonksiyonu ile iletişim kurar. Böylece, iş mantığı ve veri erişimi servis katmanında toplanır.

### b) Servis Katmanında İş Mantığı ve Veri Erişimi

Örnek: `FacilityService.create`

```python
class FacilityService:
    @staticmethod
    def create(title, district_id, city_id):
        session_db = SQLAlchemySessionSingleton.get_session()
        if not title or not district_id or not city_id:
            return {'error': 'Başlık, il ve ilçe gerekli.'}, 400
        if session_db.query(Facility).filter_by(title=title).first():
            return {'error': 'Bu isimde tesis zaten var.'}, 400
        f = Facility(title=title, district_id=district_id, city_id=city_id)
        session_db.add(f)
        session_db.commit()
        return {'id': f.id, 'name': f.title}, 201
```

Tüm iş kuralları ve veritabanı işlemleri burada kapsüllenmiştir.

### c) Diğer Servis Kullanım Örnekleri
- Kullanıcı sepetine üyelik ekleme: `ShopbagService.add_membership`
- Günlük seansları listeleme: `SessionService.get_today_sessions`
- Duyuru ekleme: `AnnouncementService.create`

## 4. Facade Katmanının Sağladığı Avantajlar
- **Karmaşıklığı Gizler:** Route'lar, model ve veritabanı detaylarını bilmek zorunda kalmaz.
- **Tek Noktadan Yönetim:** İş mantığı ve veri erişimi merkezi olarak servislerde toplanır.
- **Bakım Kolaylığı:** Değişiklikler sadece servis katmanında yapılır, üst katmanlar etkilenmez.
- **Test Edilebilirlik:** Servisler bağımsız olarak test edilebilir.
- **Yeniden Kullanılabilirlik:** Servis fonksiyonları farklı yerlerde tekrar kullanılabilir.

## 5. Akış Diyagramı

```
Kullanıcı → Flask Route → Service (Facade) → Model/DB
```

## 6. Genişletilebilirlik ve En İyi Pratikler
- Yeni bir işlev eklerken, önce ilgili servise fonksiyon eklenir, ardından route bu fonksiyonu çağırır.
- Servisler, sadece iş mantığı ve veri erişimiyle ilgilenir; HTTP, request, response gibi Flask'a özgü nesneler servis katmanına taşınmaz.
- Servisler, gerektiğinde diğer servisleri de kullanabilir (ör. bir üyelik işlemi sırasında hem kullanıcı hem tesis servisi çağrılabilir).

## 7. Sonuç
Bu projede Facade deseni, servis katmanı aracılığıyla başarıyla uygulanmıştır. Böylece, kodun okunabilirliği, sürdürülebilirliği ve genişletilebilirliği artırılmıştır. Route'lar ile model/DB arasındaki tüm iş mantığı, servislerde toplanarak modern ve ölçeklenebilir bir mimari elde edilmiştir.
