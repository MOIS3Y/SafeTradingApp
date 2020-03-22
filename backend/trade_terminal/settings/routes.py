from flask import jsonify, request, abort, url_for
from flask_praetorian import auth_required, current_user
from trade_terminal import db
from trade_terminal.settings import bp
from .models import (
    Exchange,
    Currency,
    TradeProfile,
    TradeSettings,
    TradeProfileSchema,
    TradeSettingsSchema)


@bp.route('/trade_profile/show/', methods=['GET'])
@bp.route('/trade_profile/show/<name>', methods=['GET'])
@auth_required
def show_trade_profile(name=None):

    user = current_user()

    if name:
        current_trade_profile = TradeProfile.query.filter_by(
            name=name).first()
        if current_trade_profile:
            response = TradeProfileSchema().dump(current_trade_profile)
            return jsonify(
                status_code=200,
                error='',
                trade_profile=response), 200
        else:
            return jsonify(
                status_code=200,
                error='NotFoundTradeProfile',
                trade_profile={}), 200
    if not name:
        response = TradeProfileSchema().dump(
            user.trade_profiles, many=True)
        return jsonify(
                status_code=200,
                error='',
                trade_profiles=response), 200


@bp.route('/trade_profile/create/', methods=['GET', 'POST'])
@bp.route('/trade_profile/create/<name>', methods=['POST'])
@auth_required
def create_trade_profile(name=None):

    user = current_user()
    profile_fields = request.get_json(force=True)

    # * Checking the required parameters from the user
    if not name:
        uri = url_for(
            'settings.create_trade_profile', _external=True)
        message = "Missing name in URI: {}NAME".format(uri)
        return jsonify(
            status_code=400,
            error='MissingName',
            message=message), 400

    if not profile_fields or type(profile_fields) != dict:
        abort(400)
    if profile_fields.keys() != {'exchange', 'secret_key', 'public_key'}:
        return jsonify(
            status_code=400,
            error='MissingRequiredFields',
            message='Check for required fields'), 400

    for value in profile_fields.values():
        if type(value) != str:
            return jsonify(
                status_code=400,
                error='TypeError',
                message='Type fields must be a string'), 400

    current_exchange = Exchange.query.filter_by(
        name=profile_fields['exchange'].upper()).first()
    if not current_exchange:
        return jsonify(
            status_code=400,
            error='NotSupportedExchange',
            message='The service does not support {} exchange'.format(
                profile_fields['exchange'])), 400

    check_trade_profile = TradeProfile.query.filter_by(
        name=name, user=user).first()
    if check_trade_profile:
        return jsonify(
            status_code=409,
            error='ConflictTradeProfiles',
            message='Trade Profile: {} already in use'.format(name)), 409

    # * Create new TradeProfile
    new_trade_profile = TradeProfile(
        user=user,
        exchange=current_exchange,
        name=name,
        public_key=profile_fields['public_key'],
        secret_key=profile_fields['secret_key'],
    )
    db.session.add(new_trade_profile)
    db.session.commit()
    response = TradeProfileSchema().dump(new_trade_profile)
    return jsonify(
        status_code=201,
        error='',
        new_trade_profile=response), 201


@bp.route('/trade_profile/change/', methods=['GET', 'PUT'])
@bp.route('/trade_profile/change/<name>', methods=['PUT'])
@auth_required
def change_trade_profile(name=None):

    user = current_user()
    profile_fields = request.get_json(force=True)

    # * Checking the required parameters from the user
    if not name:
        uri = url_for(
            'settings.change_trade_profile', _external=True)
        message = "Missing name in URI: {}NAME".format(uri)
        return jsonify(
            status_code=400,
            error='MissingName',
            message=message), 400
    if not profile_fields or type(profile_fields) != dict:
        abort(400)
    for value in profile_fields.values():
        if type(value) != str:
            return jsonify(
                status_code=400,
                error='TypeError',
                message='Type fields must be a string'), 400

    current_trade_profile = TradeProfile.query.filter_by(
        name=name, user=user).first()
    if current_trade_profile:
        new_name = profile_fields.get('new_name', None)
        if new_name:
            # * Check used name
            all_trade_profile = TradeProfile.query.filter_by(user=user).all()
            for profile in all_trade_profile:
                if new_name == profile.name:
                    return jsonify(
                        status_code=409,
                        error='ConflictTradeProfiles',
                        message='Trade Profile: {} already in use'.format(
                            new_name)), 409
            current_trade_profile.name = new_name

        secret_key = profile_fields.get('secret_key', None)
        if secret_key:
            current_trade_profile.secret_key = secret_key

        public_key = profile_fields.get('public_key', None)
        if public_key:
            current_trade_profile.public_key = public_key
        db.session.commit()
        response = TradeProfileSchema().dump(current_trade_profile)
        return jsonify(
                status_code=200,
                error='',
                update_trade_profile=response), 200
    if not current_trade_profile:
        return jsonify(
            status_code=400,
            error='NotFoundTradeProfile',
            message='Trade profile: {} not found'.format(name)), 400


@bp.route('/trade_profile/delete/', methods=['GET', 'DELETE'])
@bp.route('/trade_profile/delete/<name>', methods=['DELETE'])
@auth_required
def delete_trade_profile(name=None):

    user = current_user()

    # * Checking the required parameters from the user
    if not name:
        uri = url_for(
            'settings.delete_trade_profile', _external=True)
        message = "Missing name in URI: {}NAME".format(uri)
        return jsonify(
            status_code=400,
            error='MissingName',
            message=message), 400

    # * Delete TradeProfile
    delete_profile = TradeProfile.query.filter_by(
        user=user, name=name).first()
    if delete_profile:
        all_settings_trade_profile = TradeSettings.query.filter_by(
            trade_profile=delete_profile).all()
        if all_settings_trade_profile:
            for settings in all_settings_trade_profile:
                db.session.delete(settings)
        # * Make response message
        response = 'Trade profile: {}, successfully deleted'.format(
            delete_profile.name)

        db.session.delete(delete_profile)
        db.session.commit()
        return jsonify(
                status_code=200,
                error='',
                message=response), 200
    if not delete_profile:
        response = 'Check input name: {}, and try again'.format(name)
        return jsonify(
            status_code=200,
            error='NotFoundTradeProfile',
            message=response), 200


@bp.route('trade_settings/create/', methods=['POST'])
@bp.route('trade_settings/create/<name>', methods=['POST'])
@auth_required
def create_trade_settings(name=None):

    user = current_user()
    settings_fields = request.get_json(force=True)

    # * Checking the required parameters from the user
    if not name:
        uri = url_for(
            'settings.create_trade_settings', _external=True)
        message = "Missing name in URI: {}NAME".format(uri)
        return jsonify(
            status_code=400,
            error='MissingName',
            message=message), 400

    if not settings_fields or type(settings_fields) != dict:
        abort(400)

    if 'ticker' not in settings_fields or 'deposit' not in settings_fields:
        return jsonify(
            status_code=400,
            error='MissingRequiredFields',
            message='Check for required fields'), 400

    for key, value in settings_fields.items():
        if key == 'ticker':
            if type(value) != str:
                return jsonify(
                    status_code=400,
                    error='TypeError',
                    message='Type fields {} must be a string'.format(key)), 400
        else:
            if type(value) not in [int, float] or value == 0:
                return jsonify(
                    status_code=400,
                    error='TypeError',
                    message="{} must be a int or float and not equal 0".format(
                        key)), 400

    # * Checking TradeProfile and support ticker
    ticker = settings_fields.get('ticker').upper()
    current_trade_profile = TradeProfile.query.filter_by(
        name=name, user=user).first()

    if current_trade_profile:
        current_currency = Currency.query.filter_by(ticker=ticker).first()
        # TODO: fix me! current_currency may be None!!!
        if current_currency not in current_trade_profile.exchange.currencies:
            return jsonify(
                status_code=400,
                error='NotSupportedCurrency',
                message='Exchange does not support trading for {}'.format(
                    settings_fields['ticker'])), 400
        for trade_settings in current_trade_profile.trade_settings:
            if ticker == trade_settings.currency.ticker:
                return jsonify(
                    status_code=409,
                    error='ConflictTradeSettings',
                    message='Trade Settings: already in use for {}'.format(
                        ticker)), 409

    if not current_trade_profile:
        response = 'Check input name: {}, and try again'.format(name)
        return jsonify(
            status_code=200,
            error='NotFoundTradeProfile',
            message=response), 200

    # * Create new TradeSettings
    new_trade_settings = TradeSettings(
        currency=current_currency,
        trade_profile=current_trade_profile,
        ticker=ticker)

    # * Customize standart parameters of TradeSettings
    deposit = settings_fields.get('deposit')
    procent_deposit = settings_fields.get('procent_deposit', None)
    procent_risk = settings_fields.get('procent_risk', None)

    if not procent_deposit and not procent_risk:
        new_trade_settings.set_trading_parameters(deposit)
    if procent_deposit and procent_risk:
        new_trade_settings.set_trading_parameters(
            deposit, procent_deposit, procent_risk)
    if procent_deposit:
        new_trade_settings.set_trading_parameters(
            deposit, procent_deposit)
    if procent_risk:
        new_trade_settings.set_trading_parameters(
            deposit, procent_risk=procent_risk)

    db.session.add(new_trade_settings)
    db.session.commit()
    response = TradeSettingsSchema().dump(new_trade_settings)
    return jsonify(
        status_code=201,
        error='',
        new_trade_settings=response), 201


@bp.route('trade_settings/change/', methods=['PUT'])
@bp.route('trade_settings/change/<name>', methods=['PUT'])
@auth_required
def change_trade_settings(name=None):
    pass
