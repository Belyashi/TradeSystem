from trading_system.db import session
from trading_system import models as mx
from flask.views import MethodView


class BaseView(MethodView):

    def get_user(self, request):
        token = request.args.get('token')
        user = (
            session.query(mx.User)
            .select_from(mx.User)
            .join(mx.Token, mx.Token.user_id == mx.User.id)
            .filter(mx.Token.token == token)
            .first()
        )
        self.user = user
        return user
