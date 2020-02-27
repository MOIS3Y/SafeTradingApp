from trade_terminal import db


class Exchange(db.Model):
    """docstring for Exchange"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    # ! Relationship

    trade_profiles = db.relationship(
        'TradeProfile', backref='exchange', lazy=True)

    # * Exmo:
    exmo_currencies = db.relationship(
        'ExmoCurrency', backref='exchange', lazy=True)
    exmo_pairs = db.relationship(
        'ExmoPair', backref='exchange', lazy=True)

    def __repr__(self):
        return '<Exchange {}>'.format(self.name)


class TradeProfile(db.Model):
    """docstring for PrivateSettings"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))
    name = db.Column(db.String(12))
    secret_key = db.Column(db.String(128))
    public_key = db.Column(db.String(128))

    # ! Relationship

    # * Exmo:
    exmo_orders = db.relationship(
        'ExmoOrder', backref='trade_profile', lazy=True)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)
