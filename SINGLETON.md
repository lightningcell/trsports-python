# Projede Singleton Mimarisi ve Kullanımı

Bu projede veritabanı işlemlerinin yönetimi için Singleton tasarım deseni uygulanmıştır. Singleton, bir sınıfın uygulama boyunca yalnızca bir örneğinin (instance) oluşturulmasını garanti altına alır. Bu sayede, veritabanı bağlantısı ve session yönetimi merkezi ve tutarlı bir şekilde sağlanır. 

Flask-SQLAlchemy gibi klasik yaklaşımlarda her uygulama için birden fazla session veya engine örneği oluşabilir. Ancak Singleton ile, uygulamanın her yerinde aynı veritabanı bağlantısı ve session yönetimi kullanılır. Bu, hem kaynak kullanımını optimize eder hem de kodun daha okunabilir ve bakımı kolay olmasını sağlar.

Aşağıda, projede kullanılan Singleton yapısının detayları ve örnek kullanımları yer almaktadır.

# SQLAlchemySessionSingleton Kullanım Dökümantasyonu

Bu projede, SQLAlchemy ile veritabanı işlemlerini yönetmek için Singleton tasarım deseni uygulanmıştır. Tüm veritabanı bağlantısı ve oturum (session) işlemleri `db_singleton.py` dosyasındaki `SQLAlchemySessionSingleton` sınıfı üzerinden gerçekleştirilir.

## Amaç
- Tüm projede tek bir veritabanı bağlantısı ve session yönetimi sağlamak
- Flask-SQLAlchemy bağımlılığını kaldırmak ve doğrudan SQLAlchemy kullanmak
- Kodun daha okunabilir ve yönetilebilir olmasını sağlamak

## Sınıf Tanımı
`db_singleton.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

class SQLAlchemySessionSingleton:
    _engine = None
    _SessionLocal = None

    @classmethod
    def initialize(cls, db_url):
        if cls._engine is None:
            cls._engine = create_engine(db_url, echo=True)
            cls._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls._engine)
            Base.metadata.bind = cls._engine

    @classmethod
    def get_session(cls):
        if cls._SessionLocal is None:
            raise Exception("Engine is not initialized. Call initialize() first.")
        return cls._SessionLocal()
```

## Kullanım Adımları

### 1. Singleton'ı Başlatma
Projede veritabanı işlemlerine başlamadan önce **sadece bir kez** initialize edilmelidir:
```python
from db_singleton import SQLAlchemySessionSingleton
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
```
> Not: `db_url` projenizin kullandığı veritabanı bağlantı adresidir.

### 2. Session Alma
Veritabanı işlemleri için session nesnesi alınır:
```python
session = SQLAlchemySessionSingleton.get_session()
```

### 3. CRUD İşlemleri
Session üzerinden SQLAlchemy modelleriyle standart işlemler yapılır:
```python
# Kayıt ekleme
user = User(name="Ali", ...)
session.add(user)
session.commit()

# Sorgulama
user = session.query(User).filter_by(name="Ali").first()

# Güncelleme
user.name = "Veli"
session.commit()

# Silme
session.delete(user)
session.commit()
```

### 4. Örnek Kullanımlar
#### Servislerde
```python
class UserRoleService:
    @staticmethod
    def get_by_id(role_id):
        session = SQLAlchemySessionSingleton.get_session()
        return session.query(UserRole).get(role_id)
```
#### Scriptlerde
```python
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
session = SQLAlchemySessionSingleton.get_session()
for role_name in ["Admin", "User", "Student"]:
    if not session.query(UserRole).filter_by(name=role_name).first():
        session.add(UserRole(name=role_name))
session.commit()
```

### 5. Flask ile Kullanım
Flask uygulamasında, `db.init_app` ve `db.session` yerine Singleton kullanılmalıdır. Örneğin:
```python
# app.py içinde
SQLAlchemySessionSingleton.initialize('sqlite:///instance/trsports.db')
from models.base import Base
engine = SQLAlchemySessionSingleton._engine
with app.app_context():
    Base.metadata.create_all(bind=engine)
```

Kullanıcı işlemlerinde:
```python
session = SQLAlchemySessionSingleton.get_session()
user = session.query(User).get(user_id)
```

## Dikkat Edilmesi Gerekenler
- `initialize` metodu uygulama başlatılırken **yalnızca bir kez** çağrılmalıdır.
- Her işlemde yeni bir session alınabilir, işlemler bittikten sonra session kapatılabilir (isteğe bağlı).
- Flask'ın kendi `session` objesi ile isim çakışmasına dikkat edin. Kodda genellikle `session_db` veya benzeri isimler tercih edilmiştir.

## Avantajlar
- Tek noktadan veritabanı yönetimi
- Kod tekrarını azaltır
- Test ve bakım kolaylığı sağlar

---
Herhangi bir sorunda veya Singleton ile ilgili hata mesajlarında, `initialize` metodunun çağrıldığından ve bağlantı adresinin doğru olduğundan emin olun.
