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
    """docstring for TradeProfile"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    exchange_id = db.Column(db.Integer, db.ForeignKey('exchange.id'))

    name = db.Column(db.String(12))
    secret_key = db.Column(db.String(128))
    public_key = db.Column(db.String(128))

    # ! Relationship

    trade_settings = db.relationship(
        'TradeSettings', backref='trade_profile', lazy=True)
    # * Exmo:
    exmo_orders = db.relationship(
        'ExmoOrder', backref='trade_profile', lazy=True, uselist=False)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)


class TradeSettings(db.Model):
    """docstring for TradeSettings"""
    id = db.Column(db.Integer, primary_key=True)
    trade_profile_id = db.Column(
        db.Integer, db.ForeignKey('trade_profile.id'), unique=True)

    trade_deposit = db.Column(db.Float)
    risk_profit_ratio = db.Column(db.Integer)
    risk_one_day = db.Column(db.Integer)
    stop_loss_default = db.Column(db.Float)

    set_blocked = db.Column(db.Boolean)
    last_update = db.Column(db.DateTime)

    def set_trade_deposit(self, balance, procent):
        self.trade_deposit = balance / 100 * procent
        self. set_blocked = True

    def __repr__(self):
        return '<TradeSettings for : {}>'.format(self.trade_profile.name)
