from datetime import datetime
from trade_terminal import db, ma


currencies = db.Table(
    'currencies',
    db.Column(
        'currency_id',
        db.Integer,
        db.ForeignKey('currency.id'),
        primary_key=True),
    db.Column(
        'exchange_id',
        db.Integer,
        db.ForeignKey('exchange.id'),
        primary_key=True))


class Exchange(db.Model):
    """docstring for Exchange"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))

    # ! Relationship

    trade_profiles = db.relationship(
        'TradeProfile', backref='exchange', lazy=True)

    currencies = db.relationship(
        'Currency',
        secondary=currencies,
        backref=db.backref('exchanges', lazy=True))

    # * Exmo:
    # exmo_pairs = db.relationship(
    #     'ExmoPair', backref='exchange', lazy=True)

    def __repr__(self):
        return '<Exchange {}>'.format(self.name)


class Currency(db.Model):
    """docstring for Currency"""
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(12))

    def __repr__(self):
        return '<Currency {}>'.format(self.ticker)


class TradeProfile(db.Model):
    """docstring for TradeProfile"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    exchange_id = db.Column(
        db.Integer, db.ForeignKey('exchange.id'), nullable=False)

    name = db.Column(db.String(12))
    secret_key = db.Column(db.String(128))
    public_key = db.Column(db.String(128))

    # ! Relationship

    trade_settings = db.relationship(
        'TradeSettings', backref='trade_profile', lazy=True)

    # * Exmo:
    # exmo_orders = db.relationship(
    #     'ExmoOrder', backref='trade_profile', lazy=True)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)


class TradeSettings(db.Model):
    """docstring for TradeSettings"""
    id = db.Column(db.Integer, primary_key=True)
    trade_profile_id = db.Column(
        db.Integer, db.ForeignKey('trade_profile.id'), nullable=False)

    ticker = db.Column(db.String(12), nullable=False)
    trade_deposit = db.Column(db.Float, nullable=False)
    risk_profit_ratio = db.Column(db.Integer, nullable=False, default=3)
    risk_one_day = db.Column(db.Integer, nullable=False, default=1)
    stop_loss_default = db.Column(db.Float, nullable=False, default=0.5)

    set_blocked = db.Column(db.Boolean, nullable=False, default=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    def get_ticker(self, ticker):
        for currency in self.trade_profile.exchange.currencies:
            if currency.ticker == ticker:
                self.ticker = currency.ticker

    def set_trade_deposit(self, balance, procent):
        self.trade_deposit = balance / 100 * procent
        self. set_blocked = True
        self.last_update = datetime.utcnow

    def __repr__(self):
        return '<TradeSettings for : {}>'.format(self.trade_profile.name)


class TradeProfileSchema(ma.ModelSchema):
    class Meta:
        model = TradeProfile


class TradeSettingsSchema(ma.ModelSchema):
    class Meta:
        model = TradeSettings
