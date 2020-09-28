from flask import Blueprint, render_template, request, send_file

from algo_art.src.algorithm import Algorithm
from algo_art.src.main import main

# Create the home blueprint, which is registered in __init__.py
bp = Blueprint('home', __name__, url_prefix='/home')

ALGORITHM_MAP = {algo.name: algo for algo in Algorithm.__subclasses__()}

@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        algo = request.form['algo']
        main(algo)

    context = {'algorithms': [algo.name for algo in Algorithm.__subclasses__()]}
    return render_template('home.html', **context)
