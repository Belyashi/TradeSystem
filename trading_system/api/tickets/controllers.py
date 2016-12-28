import datetime
import json
from flask import request
from trading_system import models as mx
from trading_system.db import session
from trading_system.api.base_view import BaseView
from trading_system.api.utils import json_data
from trading_system.trade.tickets import open_ticket, close_ticket


class TicketsController(BaseView):

    def get(self):
        self.get_user(request)
        tickets = list(
            session.query(mx.Ticket)
            .filter(mx.Ticket.user_id == self.user.id)
        )
        return json_data(tickets)

    def post(self):
        self.get_user(request)

        required_members = (
            'stock_id', 'count', 'price', 'buy', 'duration'
        )

        data = json.loads(request.data.decode('utf-8'))

        missing_members = set(required_members) - set(data)
        if missing_members:
            return json_data(missing_members), 400

        excess_members = set(data) - set(required_members)
        if excess_members:
            return json_data(excess_members), 400

        ticket = open_ticket(
            session,
            self.user.id,
            data['stock_id'],
            data['count'],
            data['price'],
            data['buy'],
            datetime.timedelta(minutes=data['duration']),
        )

        return json_data(ticket)


class TicketController(BaseView):

    def get(self, ticket_id):
        self.get_user(request)

        ticket = session.query(
            mx.Ticket
        ).filter(
            mx.Ticket.id == ticket_id,
            mx.Ticket.user_id == self.user.id,
        ).first()

        if not ticket:
            return '', 404

        return json_data(ticket)

    def delete(self, ticket_id):
        self.get_user(request)
        ticket = session.query(
            mx.Ticket
        ).filter(
            mx.Ticket.id == ticket_id,
            mx.Ticket.user_id == self.user.id
        ).first()

        if not ticket:
            return '', 404

        close_ticket(session, ticket.id, False)

        return 'Ticket closed'
