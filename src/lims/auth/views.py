from flask import Blueprint, render_template, flash, g, session, redirect, url_for, request


from werkzeug import check_password_hash, generate_password_hash

from lims import db
from lims.auth.forms import LoginForm, RegisterForm, ForgotForm
from lims.auth.models import User

# auth = Blueprint('auth', __name__ )
# url_prefix='/auth')

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     login_form = LoginForm()
#     register_form = RegisterForm()
#
#     if request.method == 'POST' and request.form.get('login-submit', None) == 'Log In':
#         if login_form.validate_on_submit():
#             user = User.query.filter_by(email=login_form.email.data).first()
#             if user:
#                 if check_password_hash(user.password, login_form.password.data):
#                     session['user_id'] = user.id
#                     flash('Welcome %s' % user.name)
#                     return redirect(url_for(''))
#                 else:
#                     flash('Wrong Password', 'danger')
#             else:
#                 flash('You don not have account with us. Please Register.', 'danger')
#                 return redirect(url_for('auth.login'))
#
#     elif request.method == 'POST' and request.form.get('register-submit', None) == 'Register Now':
#         if register_form.validate_on_submit():
#             user = User(register_form.email.data, register_form.password.data)
#             db.session.add(user)
#
#             flash('Thanks for Registering.', 'info')
#
#             return redirect(url_for('auth/login.html'))
#
#     return render_template("auth/login.html", login_form=login_form, register_form=register_form)


# @auth.route('/forgot', methods=['GET', 'POST'])
# def forgot():
#     forgot_form = ForgotForm()
#     return render_template("auth/forgot.html", form=forgot_form)
#
#
# @auth.route('/register', methods=['GET', 'POST'])
# def register():
#     return None
