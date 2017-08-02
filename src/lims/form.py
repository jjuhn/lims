from flask_wtf import FlaskForm
from wtforms import IntegerField, RadioField, StringField, FieldList, FormField, DecimalField, TextAreaField, FileField, SelectField
from wtforms.fields.html5 import EmailField, TelField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from models import Aliquot

class SampleReceptionForm(FlaskForm):
    # neurocode_id = IntegerField('Neurocode ID', validators=[DataRequired() ])
    # age = IntegerField('Age', validators=[DataRequired()])
    # gender = RadioField('Gender', choices=[("1", 'Male'),("2", 'Female'),("3", 'Unknown')] )
    sample_type = RadioField('Sample Type', choices=[('blood','Blood'), ('saliva','Saliva'), ('DNA','DNA')])


class AddressForm(FlaskForm):
    address = StringField('Address')
    city = StringField('City')
    province = StringField('Province')
    postal_code = StringField('Postal Code')


class PhysicianForm(FlaskForm):
    first = StringField('First Name')
    last = StringField('Last Name')
    msp = IntegerField('MSP Number (BC)', id='msp')
    physician_address = StringField('Address')
    physician_city = StringField('City')
    physician_province = StringField('Province')
    physician_postal_code = StringField('Postal Code')
    # physician_institute = StringField('Institute', id='physician_institute')
    physician_phone_number = StringField('Phone Number')
    physician_fax = StringField('Fax')
    physician_email = EmailField('Email')


class SubjectForm(FlaskForm):
    neurocode_id = IntegerField('Neurocode ID')
    gender = RadioField('Gender', choices=[(1, 'Male'), (2, 'Female'), (3, 'Unknown')], coerce=int)
    age = IntegerField('Age')
    label = StringField('Label')


class NewAliquotForm(FlaskForm):
    barcode = StringField('Barcode', validators=[DataRequired()])


class LaboratoryForm(FlaskForm):
    lab_name = StringField('Facility Name', )
    lab_address = StringField('Address')
    lab_city = StringField('City')
    lab_province = StringField('Province')
    lab_postal_code = StringField('Postal Code')
    lab_phone_number = TelField('Phone Number')
    lab_fax = TelField('Fax')
    lab_contact_name = StringField('Contact Name')
    HGNC_gene_symbol = StringField('HGNC Gene Symbol')
    HGVS_protein_change = StringField('HGVS Protein Change')
    transcript_id = StringField('Transcript ID')


class ElectrophoresisForm(FlaskForm):
    aliquot = QuerySelectField(query_factory=lambda: Aliquot.query.all())
    total_volume = DecimalField("Total Volume (ul)")
    DNA_conc_abs = DecimalField("DNA Concentration (Absorbance: ng/ul)")
    DNA_conc_flr = DecimalField("DNA Concentration (Fluorescence: ng/ul)")
    DNA_qual = DecimalField("DNA Quality (260/280)")
    DNA_integrity = FileField('DNA Integrity (Gel picture)')
    notes = TextAreaField('Notes')







#
# class LoginForm(FlaskForm):
#     email = StringField('Email address', id='login-email')
#     password = PasswordField('Password', id='login-password')
#     remember_me = BooleanField('Remember me')
#     login = SubmitField('Login')
#
#
# class RegistrationForm(FlaskForm, AddressMixin):
#     email = StringField('Email Address')
#     name = StringField('Name')
#     password = PasswordField('Password')
#     confirm = PasswordField('Confirm Password')
#
#     accept = BooleanField('Accept Terms')
#
#     register = SubmitField('Register')
#
#     def validate_email(self, field):
#         if User.query.filter(User.email == field.data).first():
#             raise ValidationError("The email address: '{0}' is already registered.".format(field.data))
#
#
# class ChangePasswordForm(FlaskForm):
#     old_password = PasswordField('Old password')
#     password = PasswordField('New password')
#     confirm = PasswordField('Confirm new password')
#     change = SubmitField('Change My Password')
#
#
# class PasswordResetRequestForm(FlaskForm):
#     email = StringField('Email')
#     reset = SubmitField('Reset Password')
#
#
# class PasswordResetForm(FlaskForm):
#     email = StringField('Email')
#     password = PasswordField('New password')
#     confirm = PasswordField('Confirm password')
#     reset = SubmitField('Reset Password')