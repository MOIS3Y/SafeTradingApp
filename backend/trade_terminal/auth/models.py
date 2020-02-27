from werkzeug.security import generate_password_hash, check_password_hash
from trade_terminal import db


class User(db.Model):
    """docstring for Users """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(512))

    # ! Relationship

    trade_profiles = db.relationship(
        'TradeProfile', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
