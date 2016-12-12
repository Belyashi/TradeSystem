from flask import Flask
from . import auth, stocks


app = Flask(__name__)


app.register_blueprint(auth)
app.register_blueprint(stocks)
