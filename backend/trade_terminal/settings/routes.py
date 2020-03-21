from flask import jsonify, request, abort
from flask_praetorian import auth_required, current_user
from trade_terminal import db
from trade_terminal.settings import bp, TradeProfile, Exchange
from .models import TradeProfileSchema


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


@bp.route('/trade_profile/create/', methods=['POST'])
@bp.route('/trade_profile/create/<name>', methods=['POST'])
@auth_required
def create_trade_profile(name=None):

    user = current_user()
    profile_fields = request.get_json(force=True)

    # * Checking the required parameters from the user
    if not name:
        abort(400)
    if not profile_fields or type(profile_fields) != dict:
        abort(400)
    if profile_fields.keys() != {'exchange', 'secret_key', 'public_key'}:
        abort(400)
    for value in profile_fields.values():
        if type(value) != str:
            abort(400)
    current_exchange = Exchange.query.filter_by(
        name=profile_fields['exchange']).first()
    if not current_exchange:
        abort(400)

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


@bp.route('/trade_profile/change/', methods=['PUT'])
@bp.route('/trade_profile/change/<name>', methods=['PUT'])
@auth_required
def change_trade_profile(name=None):

    user = current_user()
    profile_fields = request.get_json(force=True)

    # * Checking the required parameters from the user
    if not name:
        abort(400)
    if not profile_fields or type(profile_fields) != dict:
        abort(400)
    for value in profile_fields.values():
        if type(value) != str:
            abort(400)

    current_trade_profile = TradeProfile.query.filter_by(
        name=name, user=user).first()
    if current_trade_profile:
        new_name = profile_fields.get('new_name', None)
        secret_key = profile_fields.get('secret_key', None)
        public_key = profile_fields.get('public_key', None)
        if new_name:
            current_trade_profile.name = new_name
        if secret_key:
            current_trade_profile.secret_key = secret_key
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
            status_code=200,
            error='NotFoundTradeProfile',
            trade_profile={}), 200


@bp.route('/trade_profile/delete/', methods=['DELETE'])
@bp.route('/trade_profile/delete/<name>', methods=['DELETE'])
@auth_required
def delete_trade_profile(name=None):

    user = current_user()

    # * Checking the required parameters from the user
    if not name:
        abort(400)

    # * Delete TradeProfile
    delete_profile = TradeProfile.query.filter_by(
        user=user, name=name).first()
    if delete_profile:
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


# @bp.route(
#   '<name>/trade_settings/<ticker>', methods=['POST', 'PUT', 'DELETE'])
# @auth_required
# def trade_settings(name):

#     # user = current_user()
#     request_data = request.get_json(force=True)
#     trade_settings = request_data.get('trade_settings', {})

#     if not trade_settings:
#         abort(400)

#     if request.method == 'POST':
#         if trade_settings and trade_settings.keys() == {
#                 'ticker',
#                 'trade_deposit',
#                 'risk_profit_ratio',
#                 'risk_one_day',
#                 'stop_loss_default'}:
#             pass
