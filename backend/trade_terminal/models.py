from werkzeug.security import generate_password_hash, check_password_hash
from trade_terminal import db


class User(db.Model):
    """docstring for Users """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(512))
    trade_terminal_profile = db.relationship(
        'TradeProfile', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)


class TradeProfile(db.Model):
    """docstring for PrivateSettings"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))
    name = db.Column(db.String(12))
    secret_key = db.Column(db.String(128))
    public_key = db.Column(db.String(128))
    user_orders = db.relationship(
        'UserOrder', backref='trade_profile', lazy=True)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)


class Exchange(db.Model):
    """docstring for Exchange"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    trade_profile = db.relationship(
        'TradeProfile', backref='exchange', lazy=True)
    currency = db.relationship(
        'Currency', backref='exchange', lazy=True)
    pair = db.relationship(
        'Pair', backref='exchange', lazy=True)

    def __repr__(self):
        return '<Exchange {}>'.format(self.name)
