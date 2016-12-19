from flask.blueprints import Blueprint
from trading_system.api.auth_middleware import auth_middleware
from .controllers import TicketsController, TicketController


tickets = Blueprint('tickets', __name__, url_prefix='/tickets')
tickets.before_request(auth_middleware)

tickets.add_url_rule('/', view_func=TicketsController.as_view('tickets_view'), methods=['GET', 'POST'])
tickets.add_url_rule('/<int:ticket_id>', view_func=TicketController('ticket_view'), methods=['GET', 'DELETE'])
