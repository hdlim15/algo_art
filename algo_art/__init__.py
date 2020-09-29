from flask import Flask
from . import home


app = Flask(__name__)

app.register_blueprint(home.bp)
