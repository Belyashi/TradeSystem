from flask import request
from flask.blueprints import Blueprint
from trading_system.api.auth_middleware import auth_middleware
from trading_system.api.utils import json_data
from trading_system.trade.balance import get_money, get_stocks
from trading_system.db import session
from trading_system import models as mx
from ..base_view import BaseView

balance = Blueprint('balance', __name__, url_prefix='/balance')
balance.before_request(auth_middleware)


class BalanceController(BaseView):

    def get(self):
        self.get_user(request)
        user_stocks = (
            session.query(mx.StockBalance)
            .filter(
                mx.StockBalance.user_id == self.user.id
            ).all()
        )
        data = {
            'money': get_money(session, self.user.id),
            'stocks': [
                {
                    'stock_id': item.stock_id,
                    'balance': get_stocks(
                        session,
                        self.user.id,
                        item.stock_id,
                    ),
                }
                for item in user_stocks
            ]
        }

        return json_data(data)

balance.add_url_rule(
    '/',
    view_func=BalanceController.as_view('tickets_view'),
    methods=['GET'],
)
