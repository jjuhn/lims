from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    CSRFProtect(app)


    return app

app = create_app()
# app.config.from_object('config')
# app.config.from_envvar('LIMS_CONFIG_PATH')
app.config.from_pyfile('config.py')


mail = Mail(app)

db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)



@app.errorhandler(404)
def not_found(error):
    return render_template('/error/404.html'), 404


# from lims.auth.views import auth
# app.register_blueprint(auth)

from flask import Blueprint

from sa_jsonapi import serializer as jsonapi





db.create_all()


from lims import views
from lims.auth.models import User, Role
from lims.models import Aliquot, Sample, Batch, Subject, BatchAliquot, Registration, Gender

from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from lims.security.forms import LIMSConfirmRegisterForm


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, register_form=LIMSConfirmRegisterForm)


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name=app.config["APP_NAME"], template_mode='bootstrap3')

# from flask_admin import BaseView, expose, AdminIndexView
# class MyHomeView(AdminIndexView):
#     @expose('/')
#     def index(self):
#         arg1 = 'Hello'
#         return self.render('admin/index.html')
#
#
# admin = Admin(index_view=MyHomeView())



# admin.add_view(MyHomeView(name='Sample Reception', endpoint='work_1', category='Work'))
# admin.add_view(MyHomeView(name='Gel Electrophoresis', endpoint='work_2', category='Work'))
# admin.add_view(MyHomeView(name='Batch Aliquots', endpoint='work_3', category='Work'))

from flask_security import current_user, login_required


class UserAdmin(ModelView):
    column_exclude_list = ('password',)
    form_excluded_columns = ('password', 'confirmed_at', 'Active', 'last_login_at', 'current_login_at', 'last_login_ip',
                             'current_login_ip', 'current_login_ip' 'login_count',)
    column_auto_select_related = True

    def is_accessible(self):
        return current_user.has_role('admin')


class RoleAdmin(ModelView):

    def is_accessible(self):
        return current_user.has_role('admin')


# admin.add_view(ModelView(User, db.session))
# admin.add_view(ModelView(Role, db.session))

admin.add_view(UserAdmin(User, db.session))
admin.add_view(RoleAdmin(Role, db.session))

admin.add_view(ModelView(Aliquot, db.session))
admin.add_view(ModelView(Sample, db.session))
admin.add_view(ModelView(Batch, db.session))
admin.add_view(ModelView(Subject, db.session))
admin.add_view(ModelView(BatchAliquot, db.session))

admin.add_view(ModelView(Registration, db.session))
admin.add_view(ModelView(Gender, db.session))



jsonapi.register_base(db.Model)


# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='jjuhn@can.ubc.ca', password='password')
#     db.session.commit()
