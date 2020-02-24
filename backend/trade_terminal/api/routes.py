from flask import jsonify
from trade_terminal.api import bp


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})
