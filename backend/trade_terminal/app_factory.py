#! /usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'MOIS3Y'


def create_app():

    # *Create Flask app
    from flask import Flask
    app = Flask(__name__)

    from config import Config, DevelopmentConfig  # noqa: F401
    app.config.from_object(DevelopmentConfig)    # ! OR Config for production

    # *Init extensions
    from trade_terminal import db, migrate, ma, guard, mail
    from trade_terminal.auth import User, is_blacklisted

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    guard.init_app(app, User, is_blacklisted=is_blacklisted)
    mail.init_app(app)

    # *Add click commands
    from commands import (
        create_exchanges,
        create_trade_profiles,
        create_users,
        create_currencies)
    app.cli.add_command(create_users)
    app.cli.add_command(create_exchanges)
    app.cli.add_command(create_trade_profiles)
    app.cli.add_command(create_currencies)

    # Auth Blueprint
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # Settings Blueprint
    from .settings import bp as settings_bp
    app.register_blueprint(settings_bp, url_prefix='/api/settings')

    # Exmo Exchange Blueprint
    from .exmo import bp as exmo_bp
    app.register_blueprint(exmo_bp, url_prefix='/api/trading/exmo/v1')

    # Errors Blueprint
    from.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app
