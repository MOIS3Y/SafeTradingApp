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
    from trade_terminal import db, ma, migrate
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    # *Add click commands
    from commands import (
        create_exchange,
        create_trade_profiles,
        create_users,
        create_pair)
    app.cli.add_command(create_users)
    app.cli.add_command(create_exchange)
    app.cli.add_command(create_pair)
    app.cli.add_command(create_trade_profiles)

    # API Blueprint
    from .api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
