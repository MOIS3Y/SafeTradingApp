# from .exmo_factory import ExmoAPI
from decimal import Decimal
from decimal import ROUND_FLOOR


def get_current_trader(user, trade_profile_id):
    """ docstring"""
    for trade_profile in user.trade_profiles:
        if trade_profile.id == trade_profile_id:
            return trade_profile


# def set_trading_settings(**params):
#     balance = params['balance']


def deal_settings(
        self, valid_params, risk, ratio, stop_standart, gap, hand_sl):
    """forms the parameters of deal"""
    ticker_1 = valid_params['trade_params']['ticker_1']
    ticker_2 = valid_params['trade_params']['ticker_2']

    pair = valid_params['trade_params']['pair']

    position = valid_params['trade_params']['position']

    price_level = valid_params['trade_params']['price_level']

    trade_deposit = valid_params['trade_params']['trade_deposit']

    risk_one_day = trade_deposit * risk / 100
    risk_one_deal = trade_deposit * risk / 100 / ratio
    stop = price_level * stop_standart / 100
    gap = price_level * stop_standart / 100 * gap / 100

    # Long position:
    if position == 'LONG':
        type_order = 'buy'
        price_open = round(price_level + gap, 8)
        if hand_sl != 0:
            sl = hand_sl
        else:
            sl = price_open - stop
        tp = price_open + (price_open-sl)*3
        # trailing = tp * trailing / 100
        # ts = tp - trailing
        alert = price_open + (price_open-sl)*2
        quantity = round(risk_one_deal / (price_open-sl), 8)
        # commission
        commission = Decimal(
            quantity * self.commission / 100).quantize(Decimal(
                "1.00000000"), ROUND_FLOOR)
        out_amount = quantity * price_open  # sum
        in_amount = quantity - float(commission)

    # Short position:
    if position == 'SHORT':
        type_order = 'sell'
        price_open = round(price_level - gap, 8)
        if hand_sl != 0:
            sl = hand_sl
        else:
            sl = price_open + stop
        tp = price_open - (sl-price_open)*3
        # trailing = tp * trailing / 100
        # ts = tp + trailing
        alert = price_open - (sl-price_open)*2
        quantity = round(risk_one_deal / (sl - price_open), 8)
        commission = Decimal(
            quantity * price_open * self.commission / 100).quantize(Decimal(
                "1.00000000"), ROUND_FLOOR)
        in_amount = quantity*price_open - float(commission)  # sum
        out_amount = quantity

    # formation of the dict of parameters
    trade_params = dict(
        trade_deposit=trade_deposit, risk_one_day=risk_one_day,
        risk_one_deal=risk_one_deal, gap=gap,
        stop=stop,                   price_level=price_level,
        ticker_1=ticker_1,           ticker_2=ticker_2,
        pair=pair,                   position=position,
        type=type_order,
        quantity=quantity,
        commission=commission,       in_amount=in_amount,
        out_amount=out_amount,       price=price_open,
        alert=alert,                 tp=tp, sl=sl, hand_sl=hand_sl
        )
    # extracting string values and converting float,decimal to 0.00000001 f
    for key, value in trade_params.items():
        if (key != 'type'
                and key != 'ticker_1'
                and key != 'ticker_2'
                and key != 'position'
                and key != 'pair'
                and key != 'default_deal'):
            trade_params.update({key: float(f'{value:.{8}f}')})

    return trade_params
