from flask import render_template, request
from . import auth


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login')
def login():
    return render_template('auth/login.html')
