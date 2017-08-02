# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField
# from wtforms.validators import DataRequired, Email, EqualTo, Length
#
#
# class LoginForm(FlaskForm):
#     email = StringField('Email Address', [Email(), DataRequired(message='Forgot your email address?')])
#     password = PasswordField('Password', [DataRequired(message='Must provide a password.')])
#
#
# class RegisterForm(FlaskForm):
#     email = StringField('Email Address', [Email(), DataRequired(message='Email Field is Required')])
#     password = PasswordField('New Password', [
#         DataRequired(),
#         EqualTo('confirm', message='Passwords must match')
#     ])
#     confirm = PasswordField('Repeat Password', [DataRequired()])
#     # accept_tos = BooleanField('I accept the TOS', [DataRequired()])
#
#
# class ForgotForm(FlaskForm):
#     email = StringField('Email Address', [Email(), DataRequired(message='Email Field is Required')])



from flask_security.forms import RegisterForm, ConfirmRegisterForm
from flask_security.forms import Required, StringField


class LIMSConfirmRegisterForm(RegisterForm):
    first_name = StringField('First Name', [Required()])
    last_name = StringField('Last Name', [Required()])
    

