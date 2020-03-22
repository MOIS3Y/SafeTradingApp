from datetime import datetime
from trade_terminal import db, ma


# * Many to many relationship Currency with Exchange models
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

    currencies = db.relationship(
        'Currency',
        secondary=currencies,
        backref=db.backref('exchanges', lazy=True))

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
        db.Integer, db.ForeignKey('exchange.id'))

    name = db.Column(db.String(12))
    secret_key = db.Column(db.String(128))
    public_key = db.Column(db.String(128))

    # ! Relationship

    user = db.relationship(
        'User', backref='trade_profiles', lazy=True)
    exchange = db.relationship(
        'Exchange', backref='trade_profiles', lazy=True)

    def __repr__(self):
        return '<Name: {}>'.format(self.name)


class TradeSettings(db.Model):
    """docstring for TradeSettings"""
    id = db.Column(db.Integer, primary_key=True)
    trade_profile_id = db.Column(
        db.Integer, db.ForeignKey('trade_profile.id'))
    currency_id = db.Column(
        db.Integer, db.ForeignKey('currency.id'))

    ticker = db.Column(db.String(12))
    trade_deposit = db.Column(db.Float)
    risk_profit_ratio = db.Column(db.Integer, default=3)
    risk_one_day = db.Column(db.Integer, default=1)

    set_blocked = db.Column(db.Boolean, default=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    # ! Relationship

    trade_profile = db.relationship(
        'TradeProfile', backref='trade_settings', lazy=True)
    currency = db.relationship('Currency', lazy=True)

    def set_trade_deposit(self, balance, procent):
        self.trade_deposit = balance / 100 * procent
        self. set_blocked = True
        self.last_update = datetime.utcnow()

    def __repr__(self):
        return '<TradeSettings: {} for {}>'.format(
            self.trade_profile.name, self.currency.ticker)


class CurrencySchema(ma.ModelSchema):
    class Meta:
        model = Currency


class ExchangeSchema(ma.ModelSchema):
    currencies = ma.Nested(CurrencySchema, many=True)

    class Meta:
        model = Exchange


class TradeSettingsSchema(ma.ModelSchema):
    class Meta:
        model = TradeSettings


class TradeProfileSchema(ma.SQLAlchemySchema):
    trade_settings = ma.Nested(TradeSettingsSchema, many=True)
    exchange = ma.Nested(ExchangeSchema)

    class Meta:
        model = TradeProfile
        exclude = [
            'exchange.currencies',
            'exchange.trade_profiles',
            'trade_settings.trade_profile'
        ]

    id = ma.auto_field()
    name = ma.auto_field()
    public_key = ma.auto_field()
