from flask import Blueprint, render_template

from algo_art.src.algorithm import Algorithm

# Create the home blueprint, which is registered in __init__.py
bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/', methods=('GET',))
def home():
    context = {'algorithms': [algo.name for algo in Algorithm.__subclasses__()]}
    return render_template('home.html', **context)
