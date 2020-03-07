import os
from pathlib import Path  # !Only Python 3.4+(Standart library)
from dotenv import load_dotenv

from flask import Blueprint

# * Create Blueprint
bp = Blueprint('exmo', __name__)


# * Search .env file for this script work
path = Path(os.path.abspath(os.path.dirname(__file__)))
basedir = path.parents[2-1]  # * Level UP 2 directory
load_dotenv(os.path.join(basedir, '.env'))


class ExmoAPI(object):
    """
    Initializes the API requests to
    the cryptocurrency stock exchange Exmo.me
    """

    # ! API methods:
    commands = {
        # Public API
        'trades':                 {'authenticated': False},
        'order_book':             {'authenticated': False},
        'ticker':                 {'authenticated': False},
        'pair_settings':          {'authenticated': False},
        'currency':               {'authenticated': False},
        # Authenticated API
        'user_info':              {'authenticated': True},
        'order_create':           {'authenticated': True},
        'order_cancel':           {'authenticated': True},
        'user_open_orders':       {'authenticated': True},
        'user_trades':            {'authenticated': True},
        'user_cancelled_orders':  {'authenticated': True},
        'order_trades':           {'authenticated': True},
        'trade_deposit_address':  {'authenticated': True},
        # Wallet API
        'wallet_history':         {'authenticated': True}
        }

    def __init__(self, API_KEY='', API_SECRET=''):
        """Announces required parameters"""
        self.API_URL = 'https://api.exmo.me/'
        self.API_VERSION = 'v1/'
        self.API_KEY = API_KEY
        self.API_SECRET = bytes(API_SECRET, encoding='utf-8')

    def __getattr__(self, name):
        """Gets api_method"""
        def response_exmo(*args, **kwargs):
            """Gets api_params"""
            kwargs.update(command=name)
            return self.call_api(**kwargs)
        return response_exmo

    def make_sign_sha512(self, data):
        """
        When using a POST request.
        Encrypts transmitted data by signing
        with a secret key using the HMAC-SHA512 method.
        """
        from hmac import new
        from hashlib import sha512
        hash_key = new(key=self.API_SECRET, digestmod=sha512)
        hash_key.update(data.encode('utf-8'))
        return hash_key.hexdigest()

    def check_error_request(call_api):
        """
        The decorator of the call_api function.
        Checks if an exception occurred while requesting.
        If yes then returns the error name
        """
        def wrapper(*args, **kwargs):
            """
            Wraps the called function. Allows you to pass arguments to it.
            """
            # Make an exchange request
            try:
                response = call_api(*args, **kwargs)
                return response
            except Exception as error:
                error_response = {
                    'result': False,
                    'error': type(error).__name__}
                return error_response
        return wrapper

    @check_error_request
    def call_api(self, **kwargs):
        """API request"""
        from time import time
        from requests import Session
        from urllib import parse
        from json import loads

        command = kwargs.pop('command')
        params = kwargs
        uri = self.API_URL + self.API_VERSION + command
        # * Open session
        with Session() as session:
            # * POST
            if self.commands[command]['authenticated']:
                nonce = {'nonce': int(time()*1000)}
                params.update(nonce)
                params = parse.urlencode(params)
                sign = self.make_sign_sha512(params)
                headers = {
                    "Content-type": "application/x-www-form-urlencoded",
                    "Key": self.API_KEY,
                    "Sign": sign}
                exmo_request = session.post(uri, data=params, headers=headers)
                session.close()
            # * GET
            else:
                params = parse.urlencode(params)
                exmo_request = session.get(uri + '/?' + params)
                session.close()
        response = loads(exmo_request.text)
        return response


if __name__ == "__main__":
    from json import dumps
    test_request = ExmoAPI(
        API_KEY=os.environ.get('EXCHANGE_PK') or 'K-pass',
        API_SECRET=os.environ.get('EXCHANGE_SK') or 'S-pass')

    post_request = test_request.user_trades(pair='ETC_RUB')
    get_request = test_request.currency()

    print(dumps(
        post_request,
        sort_keys=False,
        indent=2,
        separators=(',', ': ')))

    # print(json.dumps(
    #     get_request,
    #     sort_keys=False,
    #     indent=2,
    #     separators=(',', ': ')))
