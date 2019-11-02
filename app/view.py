from flask import Blueprint, render_template

view = Blueprint('root', __name__, url_prefix='/')


@view.route('/')
def index():
    return render_template('index.html', tab='top')


@view.route('/notification')
def notification():
    return render_template('notification.html', tab='notification')


@view.route('/kanpo')
def kanpo():
    return render_template('kanpo.html', tab='kanpo')


@view.route('/guidance')
def guidance():
    return render_template('guidance.html', tab='guidance')


@view.route('/access')
def access():
    return render_template('access.html', tab='access')


@view.route('/consulting')
def consulting():
    return render_template('consulting.html', tab='consulting')


@view.route('/necessity')
def necessity():
    return render_template('necessity.html')


# 購入後に送るページ (リンクなし)
@view.route('/notice')
def notice():
    return render_template('notice.html')


@view.route('/list/<path:filename>')
def disease_list(filename):
    return render_template(f'disease_list/{filename}.html')


# TODO
@view.route('/yakusei')
def yakusei():
    # http://www.seisindo.com/yakusei.htm
    return render_template('yakusei.html')
