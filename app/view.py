from flask import Blueprint, render_template

view = Blueprint('root', __name__, url_prefix='/')


@view.route('/')
def index():
    return render_template('index.html')

@view.route('/hoge')
def hoge():
    return render_template('hoge.html')
