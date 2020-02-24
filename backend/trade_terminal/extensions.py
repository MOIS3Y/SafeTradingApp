from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


# *SQL DataBase
db = SQLAlchemy()
migrate = Migrate()


# *Marshmallow /Converting Flask-SQLAlchemy to JSON/
ma = Marshmallow()
