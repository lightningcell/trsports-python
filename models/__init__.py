# models paket modülü
# db örneği ve tüm modeller bu paket üzerinden import edilir

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Ara tablolar
from .associations import user_userrole, sport_facility

# Modeller
from .user import User
from .shopbag import Shopbag
from .user_information import UserInformation
from .user_role import UserRole
from .city import City
from .district import District
from .facility import Facility
from .sport import Sport
from .membership import Membership
from .train_session import TrainSession
from .announcement import Announcement 