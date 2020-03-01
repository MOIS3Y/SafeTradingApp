from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_mail import Mail


# *SQL DataBase
db = SQLAlchemy()
migrate = Migrate()

# *Marshmallow /Converting Flask-SQLAlchemy to JSON/
ma = Marshmallow()

#  * Guard API
guard = Praetorian()

#  * Mail sender
mail = Mail()
