from flask import Blueprint, render_template

view = Blueprint('root', __name__, url_prefix='/')


@view.route('/')
def index():
    return render_template('index.html')


@view.route('/notification')
def notification():
    return render_template('notification.html')


@view.route('/kanpo')
def kanpo():
    return render_template('kanpo.html')


@view.route('/guidance')
def guidance():
    return render_template('guidance.html')


@view.route('/list/hunin')
def list_hunin():
    return render_template('disease_list/hunin.html')
