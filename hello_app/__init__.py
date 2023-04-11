from flask import Flask
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app, configure_jinja=True)
