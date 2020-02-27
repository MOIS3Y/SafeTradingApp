from flask import jsonify
from trade_terminal.auth import bp


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})
