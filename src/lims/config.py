APP_NAME = 'Neurocode LIMS'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'super-secret'


# SQLALCHEMY_DATABASE_URI = 'sqlite:////Applications/PyCharm.app/Contents/bin/lims.sqlite'
SQLALCHEMY_DATABASE_URI = 'postgresql://jj@localhost/lims'
SQLALCHEMY_TRACK_MODIFICATIONS = True
# SQLALCHEMY_ECHO = True


MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = 'neurocode.labs@gmail.com'
MAIL_PASSWORD = 'QWER1234'

SECURITY_PASSWORD_HASH = 'sha512_crypt'
SECURITY_PASSWORD_SALT = ''


SECURITY_CONFIRMABLE = True
SECURITY_TRACKABLE = True
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = True


SECURITY_EMAIL_SENDER = 'neurocode.labs@gmail.com'