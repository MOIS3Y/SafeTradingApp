import os
import click
from flask.cli import with_appcontext

from trade_terminal import db
from trade_terminal.settings import TradeProfile, Currency, Exchange
from trade_terminal.auth import User
# from trade_terminal.exmo import ExmoPair


@click.command(name='create_database')
@with_appcontext
def create_database():
    db.create_all()


@click.command(name='create_users')
@with_appcontext
def create_users():
    user = User(
        username='livermore',
        roles='trader')
    user.set_password('jesse')
    print('Created: ', user.__repr__())
    admin = User(
        username='administrator',
        roles='admin, trader')
    admin.set_password('admin')
    print('Created: ', admin.__repr__())

    db.session.add_all([user, admin])
    db.session.commit()


@click.command(name='create_exchanges')
@with_appcontext
def create_exchanges():
    exmo = Exchange(name='EXMO')
    print('Created: ', exmo.__repr__())
    binance = Exchange(name='BINANCE')
    print('Created: ', binance.__repr__())

    db.session.add_all([exmo, binance])
    db.session.commit()


@click.command(name='create_trade_profile')
@with_appcontext
def create_trade_profiles():
    from dotenv import load_dotenv
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '.env'))
    secret_key = os.environ.get('EXCHANGE_SK') or 'S-pass'
    public_key = os.environ.get('EXCHANGE_PK') or 'K-pass'

    first = TradeProfile(
        user_id=1,
        exchange_id=1,
        name='TestAcc',
        exchange_name='EXMO',
        secret_key=secret_key,
        public_key=public_key)

    db.session.add(first)
    db.session.commit()
    print('Created: ', first.__repr__())


@click.command(name='create_currencies')
@with_appcontext
def create_currencies():
    currencies_list = ['BTC', 'ETH', 'RUB', 'USD']
    exchanges_list = Exchange.query.all()
    for currency in currencies_list:
        add_currency = Currency(ticker=currency)
        for exchange in exchanges_list:
            add_currency.exchanges.append(exchange)
        db.session.add(add_currency)
        db.session.commit()
        print('Created: ', add_currency.__repr__())


# @click.command(name='create_pairs')
# @with_appcontext
# def create_pairs():
#     eth_rub = ExmoPair(exchange_id=1, ticker='ETH_RUB')
#     print('Created: ', eth_rub.__repr__())
#     btc_rub = ExmoPair(exchange_id=1, ticker='BTC_RUB')
#     print('Created: ', btc_rub.__repr__())

#     db.session.add_all([eth_rub, btc_rub])
#     db.session.commit()


if __name__ == "__main__":
    print(os.environ.get('EXCHANGE_SK'))
