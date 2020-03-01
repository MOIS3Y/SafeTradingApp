from trade_terminal import db
from trade_terminal import guard


class User(db.Model):
    """docstring for Users """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(512))
    email = db.Column(db.String(120), unique=True)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default='true')

    # ! Relationship

    trade_profiles = db.relationship(
        'TradeProfile', backref='user', lazy=True)

    # ! Guard Flask-Praetorian help methods

    @property
    def rolenames(self):
        try:
            return self.roles.split(',')
        except Exception:
            return []

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    def set_password(self, password):
        self.password = guard.hash_password(password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
