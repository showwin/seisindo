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


@view.route('/list/<path:filename>')
def disease_list(filename):
    return render_template(f'disease_list/{filename}.html')


# TODO
@view.route('/yakusei')
def yakusei():
    # http://www.seisindo.com/yakusei.htm
    return render_template('yakusei.html')
