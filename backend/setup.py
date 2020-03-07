from trade_terminal import guard
from trade_terminal import create_app
from trade_terminal import db, ma
from trade_terminal import TradeProfile, TradeSettings, Exchange
from trade_terminal.auth import User
from trade_terminal.exmo import ExmoCurrency, ExmoPair, ExmoOrder


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """ To work with the application in the terminal.
        Helps not create module imports manually.
        To start, run the commands in terminal:
        $ export FLASK_APP=setup.py
        $ flask shell
        Simple example:
        >>>db
        <SQLAlchemy engine=sqlite:////path_to_db/......
        >>>Example
        <class 'app_template.models.Example'> """
    return {
        'db': db,
        'ma': ma,
        'User': User,
        'TradeProfile': TradeProfile,
        'TradeSettings': TradeSettings,
        'Exchange': Exchange,
        'ExmoCurrency': ExmoCurrency,
        'ExmoPair': ExmoPair,
        'ExmoOrder': ExmoOrder,
        'guard': guard
        }  # Add more variables {name:variable}


if __name__ == "__main__":
    app.run()
