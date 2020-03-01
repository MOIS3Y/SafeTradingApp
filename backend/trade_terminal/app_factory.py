#! /usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'MOIS3Y'


def create_app():  # ! OR Config for production

    # *Create Flask app
    from flask import Flask
    app = Flask(__name__)

    from config import Config, DevelopmentConfig  # noqa: F401
    app.config.from_object(DevelopmentConfig)

    # *Init extensions
    from trade_terminal import db, migrate, ma, guard, mail
    from trade_terminal.auth import User
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    guard.init_app(app, User)
    mail.init_app(app)

    # *Add click commands
    from commands import (
        create_exchanges,
        create_trade_profiles,
        create_users,
        create_pairs)
    app.cli.add_command(create_users)
    app.cli.add_command(create_exchanges)
    app.cli.add_command(create_pairs)
    app.cli.add_command(create_trade_profiles)

    # Auth Blueprint
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Exmo Exchange Blueprint
    from .exmo import bp as exmo_bp
    app.register_blueprint(exmo_bp, url_prefix='/api/trading/exmo/v1')

    # Errors Blueprint
    from.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
