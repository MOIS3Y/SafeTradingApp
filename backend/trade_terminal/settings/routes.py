from flask import jsonify, request
from flask_praetorian import auth_required, current_user
from trade_terminal.settings import bp


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})


@bp.route('/trade_profile', methods=['GET', 'POST', 'PUT'])
@auth_required
def trade_profile():

    user = current_user()

    if request.method == 'GET':
        trade_profiles = user.trade_profiles
        if trade_profiles:
            for profile in trade_profiles:
                # TODO: ma serialize to JSON
                return jsonify(
                    {

                    }
                )
        else:
            return jsonify(
                {

                }
            )
