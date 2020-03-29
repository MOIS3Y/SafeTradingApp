from datetime import datetime
from flask_marshmallow.fields import AbsoluteURLFor, fields
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
    exchange_name = db.Column(db.String(12))
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

    currency_ticker = db.Column(db.String(12))
    trade_deposit = db.Column(db.Float)
    risk_one_deal = db.Column(db.Float)

    set_blocked = db.Column(db.Boolean, default=False)
    last_update = db.Column(db.DateTime, default=datetime.utcnow)

    # ! Relationship

    trade_profile = db.relationship(
        'TradeProfile', backref='trade_settings', lazy=True)
    currency = db.relationship('Currency', lazy=True)

    def set_trading_parameters(
            self, deposit, procent_deposit=70, procent_risk=1):

        self.trade_deposit = round(deposit / 100 * procent_deposit, 8)
        self.risk_one_deal = round(
            self.trade_deposit * procent_risk / 100 / 3, 8)
        # * Block updating trading parameters to the new month
        self. set_blocked = True
        self.last_update = datetime.utcnow()

    def __repr__(self):
        return '<TradeSettings: {} for {}>'.format(
            self.trade_profile.name, self.currency.ticker)


class CurrencySchema(ma.ModelSchema):
    class Meta:
        model = Currency


class ExchangeSchema(ma.SQLAlchemySchema):
    # currencies = ma.Nested(CurrencySchema, many=True)

    class Meta:
        model = Exchange
    # name = ma.auto_field()


class TradeSettingsSchema(ma.SQLAlchemySchema):

    class Meta:
        model = TradeSettings

    currency = fields.Method(serialize='_change_currency_id_to_name')
    last_update = fields.Method(serialize='_change_last_update_to_timestump')
    risk_one_deal = ma.auto_field()
    set_blocked = ma.auto_field()
    trade_deposit = ma.auto_field()

    def _change_currency_id_to_name(self, model):
        return model.currency.ticker

    def _change_last_update_to_timestump(self, model):
        convert = round(model.last_update.timestamp())
        return convert


class TradeProfileSchema(ma.SQLAlchemySchema):
    # trade_settings = ma.Nested(
    #     TradeSettingsSchema, many=True, exclude=[
    #         'id', 'currency', 'trade_profile'])

    class Meta:
        model = TradeProfile
        # include_fk = True
        # exclude = [
        #     'exchange.currencies',
        #     'exchange.trade_profiles',
        #     'trade_settings.trade_profile'
        # ]

    uri = AbsoluteURLFor('settings.show_trade_profile', name='<name>')
    name = ma.auto_field()
    public_key = ma.auto_field()
    secret_key = fields.Method(serialize='_hide_secret_key')
    exchange = fields.Method(serialize='_change_exchange_id_to_name')
    trade_settings = fields.Method(serialize='_beautify_trade_settings')

    def _change_exchange_id_to_name(self, model):
        return model.exchange.name

    def _hide_secret_key(self, model):
        last_symbols = len(model.secret_key) - 2
        hide = model.secret_key[0:4] + '***' + model.secret_key[last_symbols:]
        return hide

    def _beautify_trade_settings(self, model):
        return TradeSettingsSchema().dump(model.trade_settings, many=True)
    # exchange = ma.HyperlinkRelated(
    #     'settings.show_trade_profile',
    #     url_key='exchange.name',
    #     external=True)
