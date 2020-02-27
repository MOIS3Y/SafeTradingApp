from flask import jsonify
from trade_terminal.exmo import bp


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})
