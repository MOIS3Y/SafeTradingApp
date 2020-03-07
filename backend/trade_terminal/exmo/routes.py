from flask import jsonify, request, abort
from flask_praetorian import auth_required, current_user
# from trade_terminal import TradeProfile
from .exmo_factory import bp, ExmoAPI
from .trading import get_current_trader


@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong!'})


@bp.route('/order/create', methods=['POST'])
@auth_required
def create_order():
    """
    pair - currency pair
    quantity - quantity for the order
    price - price for the order
    type - type of order, can have the following values:
        buy - buy order
        sell - sell order
        market_buy - market buy-order
        market_sell - market sell-order
        market_buy_total - market buy-order for a certain amount
        market_sell_total - market sell-order for a certain amount
    """
    input_data = request.get_json(force=True)

    trade_profile_id = input_data.get('trade_profile_id', None)
    pair = input_data.get('pair', None)
    type_order = input_data.get('type', None)
    price = input_data.get('price', None)
    stop_loss = input_data.get('stop_loss', None)

    # * Check input data
    if type(price) != (float or int):
        abort(400)
    if type(stop_loss) != (float or None):
        abort(400)

    user = current_user()
    current_trader = get_current_trader(user, trade_profile_id)

    if current_trader:
        # open_deal =
        api = ExmoAPI(
            API_KEY=current_trader.public_key,
            API_SECRET=current_trader.secret_key)
    else:
        abort(400)

    make_order = api.order_create(
        pair=pair,
        # quantity=quantity,
        price=price,
        type=type_order
    )
    return jsonify(make_order)
