from flask import jsonify, make_response
from trade_terminal.errors import bp


# ! 4xx: Client Error

@bp.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify(
        {
            'status_code': 400,
            'error': 'BadRequest',
            'message': 'Invalid request parameters'
        }), 400)


@bp.app_errorhandler(404)
def not_found(error):
    return make_response(
        jsonify(
            {
                'status_code': 404,
                'error': 'NotFound',
                'message': 'Could not find the requested path'
            }), 404)


@bp.app_errorhandler(405)
def method_not_allowed(error):
    return make_response(jsonify(
        {
            'status_code': 405,
            'error': 'MethodNotAllowed',
            'message': 'Requested method not allowed'
        }), 405)
