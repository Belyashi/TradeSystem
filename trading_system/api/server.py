from flask import Flask
from . import auth, balance, stocks, tickets


app = Flask(__name__)


app.register_blueprint(auth)
app.register_blueprint(balance)
app.register_blueprint(stocks)
app.register_blueprint(tickets)
