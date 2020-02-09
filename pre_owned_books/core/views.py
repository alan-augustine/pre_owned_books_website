from flask import render_template, Blueprint

core_blueprint = Blueprint('core_blueprint',__name__)

@core_blueprint.route('/')
def index():
    # default template file path is templates directory relative to app.py
    return render_template('home.html')
