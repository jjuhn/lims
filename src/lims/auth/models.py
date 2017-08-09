from lims import db
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from sqlalchemy.ext.hybrid import hybrid_property
from nameparser import HumanName


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# class User(UserMixin, Base):
#     __tablename__ = 'auth_user'
#
#     email = db.Column(db.String(128), nullable=False, unique=True)
#     password = db.Column(db.String(128), nullable=False)
#
#     def __init__(self, email, password):
#         self.email = email
#         self.password = password



roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return '<Role id=%s name=%s>' %(self.id, self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())

    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(255))
    current_login_ip = db.Column(db.String(255))
    login_count = db.Column(db.Integer)

    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))

    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    aliquots = db.relationship('Aliquot', backref='user')
    batches = db.relationship('Batch', backref='user')

    def __str__(self):
        return '<User id=%s email=%s>' % (self.id, self.email)


# class Physician(User):
#     __mapper_args__ = {'polymorphic_identity': 'physician'}
#
#     msp = db.Column(db.Integer, unique=True)

