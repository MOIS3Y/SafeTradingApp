from flask import jsonify, request, abort
from flask_praetorian import auth_required, current_user
from trade_terminal import db
from trade_terminal.settings import bp, TradeProfile, Exchange
from .models import TradeProfileSchema


@bp.route('/trade_profile', methods=['GET', 'POST', 'PUT', 'DELETE'])
@auth_required
def trade_profile():

    user = current_user()
    request_data = request.get_json(force=True)
    trade_profile = request_data.get('trade_profile', {})
    trade_settings = request_data.get('trade_settings', {})

    # ! API Methods:

    if request.method == 'GET':
        response = TradeProfileSchema().dump(user.trade_profiles, many=True)
        return jsonify(
                status_code=200,
                error='',
                trade_profiles=response), 200

    if request.method == 'POST':
        # * Checking the required parameters from the user
        if trade_profile and trade_profile.keys() == {
                'name', 'exchange', 'secret_key', 'public_key'}:
            # * Get current Exchange
            current_exchange = Exchange.query.filter_by(
                name=trade_profile['exchange']).first()
            # * Check Exchange
            if current_exchange:
                # * Create new TradeProfile
                new_trade_profile = TradeProfile(
                    user=user,
                    exchange=current_exchange,
                    name=trade_profile['name'],
                    public_key=trade_profile['public_key'],
                    secret_key=trade_profile['secret_key'],
                )
                db.session.add(new_trade_profile)
                db.session.commit()
                response = TradeProfileSchema().dump(new_trade_profile)
                return jsonify(
                        status_code=201,
                        error='',
                        new_trade_profile=response), 201

        if trade_settings:
            pass
        abort(400)

    if request.method == 'DELETE':
        if trade_profile and 'name' in trade_profile:
            delete_profile = TradeProfile.query.filter_by(
                user=user,
                name=trade_profile['name']).first()
            if delete_profile:
                db.session.delete(delete_profile)
                db.session.commit()
                return jsonify(
                        status_code=200,
                        error='',
                        message='Success'), 200

        if trade_settings:
            pass
        abort(400)
